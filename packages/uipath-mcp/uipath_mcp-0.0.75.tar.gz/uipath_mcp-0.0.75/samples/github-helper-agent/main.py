import json
import os
from contextlib import asynccontextmanager
from typing import Optional

import dotenv
from langchain_anthropic import ChatAnthropic
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from mcp import ClientSession
from mcp.client.sse import sse_client
from pydantic import Field

dotenv.load_dotenv()


class PullRequestState(AgentState):
    """State for the GitHub Assistant agent."""

    owner: str
    repo: str
    pullNumber: int
    in_reply_to: Optional[int]
    command: str = Field(default="review")


@asynccontextmanager
async def make_graph():
    async with sse_client(
        url=os.getenv("UIPATH_MCP_SERVER_URL"),
        headers={"Authorization": f"Bearer {os.getenv('UIPATH_ACCESS_TOKEN')}"},
        timeout=60,
    ) as (read, write):
        async with ClientSession(read, write) as session:
            tools = await load_mcp_tools(session)

            model = ChatAnthropic(model="claude-3-5-sonnet-latest")

            # Create the conversation history
            async def hydrate_history(state: PullRequestState) -> PullRequestState:
                """Fetch PR context at the start of the workflow."""
                owner = state["owner"]
                repo = state["repo"]
                pull_number = state["pullNumber"]
                command = state["command"]
                in_reply_to = state["in_reply_to"] if "in_reply_to" in state else None

                context_messages = []

                # Fetch PR details
                tool_result = await session.call_tool(
                    "get_pull_request",
                    {
                        "owner": owner,
                        "repo": repo,
                        "pullNumber": pull_number,
                    },
                )

                pr_details = json.loads(tool_result.content[0].text)

                # Add PR details as a system message
                context_messages.append(
                    {
                        "role": "system",
                        "content": f"Pull Request #{pull_number} by {pr_details['user']['login']}\nTitle: {pr_details['title']}\nDescription: {pr_details['body']}",
                    }
                )
                # Fetch PR comments
                tool_result = await session.call_tool(
                    "get_pull_request_comments",
                    {
                        "owner": owner,
                        "repo": repo,
                        "pullNumber": pull_number,
                    },
                )

                comments = json.loads(tool_result.content[0].text)

                # Add each comment as a user or assistant message
                for comment in comments:
                    # Bot comments
                    if comment["body"].startswith("/ai generated"):
                        context_messages.append(
                            {
                                "role": "assistant",
                                "content": comment["body"]
                                .replace("/ai generated", "")
                                .strip(),
                            }
                        )
                    # User comments
                    else:
                        context_messages.append(
                            {"role": "user", "content": comment["body"].strip()}
                        )
                # Fetch PR review comments
                review_comments = await session.call_tool(
                    "get_pull_request_reviews",
                    {
                        "owner": owner,
                        "repo": repo,
                        "pullNumber": pull_number,
                    },
                )

                review_comments = json.loads(tool_result.content[0].text)

                # Add review comments as messages
                for comment in review_comments:
                    if comment["body"].startswith("/ai generated"):
                        context_messages.append(
                            {
                                "role": "assistant",
                                "content": comment["body"]
                                .replace("/ai generated", "")
                                .strip(),
                            }
                        )
                    else:
                        context_messages.append(
                            {
                                "role": "user",
                                "content": f"Comment on {comment['path']} line {comment['line']}: {comment['body']}",
                            }
                        )
                    # Add the input message as the last user message
                    if in_reply_to:
                        context_messages.append(
                            {
                                "role": "user",
                                "content": f"The command is {command} with review comment id #{in_reply_to}",
                            }
                        )
                    else:
                        context_messages.append(
                            {
                                "role": "user",
                                "content": f"Please {command} this PR and provide detailed feedback.",
                            }
                        )

                # Update the state with the hydrated conversation history
                return {**state, "messages": context_messages}

            def pr_prompt(state: PullRequestState):
                """Create a prompt that incorporates PR data and the requested command."""
                system_message = f"""You are a professional developer with experience in code reviews and GitHub pull requests.
                You are working with repo: {state["owner"]}/{state["repo"]}, PR #{state["pullNumber"]}.

                IMPORTANT INSTRUCTIONS:
                1. ALWAYS get the contents of the changed files in the current PR
                2. ALWAYS use the contents of the changed files as context when replying to a user command.
                3. Always start your responses with "/ai generated" to properly tag your comments.
                4. When you reply to a comment, make sure to address the specific request.
                5. When reviewing code, be thorough but constructive - point out both issues and good practices.
                6. You MUST use the available tools to post your response as a PR comment or perform the PR code review.

                COMMANDS YOU SHOULD UNDERSTAND:
                - "review": Perform a full code review of the PR
                - "summarize": Summarize the changes in the PR
                - "explain <file>": Explain what changes were made to a specific file
                - "suggest": Suggest improvements to the code
                - "test": Suggest appropriate tests for the changes

                WORKFLOW:
                1. Gather the contents of the changed files for the current PR
                2. Analyze the available PR data and understand what the user is asking for
                3. Use the appropriate tools to gather any additional information needed
                4. Prepare your response based on the request
                5. Based on the user's command:
                    - if the command has a review comment id, REPLY TO THE REVIEW COMMENT WITH THE SPECIFIED ID
                    - else POST PULL REQUEST REVIEW

                Remember: The user wants specific, actionable feedback and help with their code.
                """

                return [{"role": "system", "content": system_message}] + state[
                    "messages"
                ]

            # Create the agent node - this will handle both analysis and posting the response
            # using its available GitHub tools
            agent = create_react_agent(
                model, tools=tools, state_schema=PullRequestState, prompt=pr_prompt
            )

            # Create a simple two-node StateGraph
            workflow = StateGraph(PullRequestState)

            # Add nodes
            workflow.add_node("hydrate_history", hydrate_history)
            workflow.add_node("agent", agent)

            # Add edges - simple linear flow from context hydration to agent to end
            workflow.add_edge("__start__", "hydrate_history")
            workflow.add_edge("hydrate_history", "agent")
            workflow.add_edge("agent", END)

            # Compile the graph
            graph = workflow.compile()

            yield graph
