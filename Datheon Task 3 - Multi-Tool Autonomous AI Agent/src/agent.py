
import os

from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import TOOLS


def build_agent():
    """Create the autonomous AI agent with three tools."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found. Please check your .env file."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=api_key,
        temperature=0,
        max_retries=2
    )

    agent = create_agent(
        model=llm,
        tools=TOOLS,
        system_prompt=(
            "You are a helpful autonomous AI assistant. "
            "Choose and use tools whenever needed. "
            "Use web_search for internet searches and current information. "
            "Use calculator for mathematical calculations. "
            "Use read_local_file to answer questions about local documents. "
            "For multi-step tasks, use multiple tools when appropriate. "
            "Never invent tool results. "
            "Give clear and simple answers."
        )
    )

    return agent


def ask_agent(agent, question):
    """Send a question to the agent and return its final answer."""

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    last_ai_message = next(
        (
            message
            for message in reversed(result["messages"])
            if getattr(message, "type", None) == "ai"
        ),
        None
    )

    if last_ai_message is None:
        return "No answer generated."

    content = last_ai_message.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        text_parts = [
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        return "\n".join(text_parts)

    return str(content)


def ask_agent_with_tools(agent, question):
    """Get the agent's answer and actual tool execution history."""

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    messages = result["messages"]

    # Extract tools that were actually executed
    used_tools = []

    for message in messages:
        if getattr(message, "type", None) == "tool":
            tool_name = getattr(message, "name", None)

            if tool_name and tool_name not in used_tools:
                used_tools.append(tool_name)

    # Extract the final AI response
    last_ai_message = next(
        (
            message
            for message in reversed(messages)
            if getattr(message, "type", None) == "ai"
        ),
        None
    )

    if last_ai_message is None:
        answer = "No answer generated."
    else:
        content = last_ai_message.content

        if isinstance(content, str):
            answer = content

        elif isinstance(content, list):
            text_parts = [
                block.get("text", "")
                for block in content
                if isinstance(block, dict)
                and block.get("type") == "text"
            ]
            answer = "\n".join(text_parts)

        else:
            answer = str(content)

    return answer, used_tools


def ask_agent(agent, question):
    """Return only the final answer for console usage."""

    answer, _ = ask_agent_with_tools(agent, question)
    return answer

