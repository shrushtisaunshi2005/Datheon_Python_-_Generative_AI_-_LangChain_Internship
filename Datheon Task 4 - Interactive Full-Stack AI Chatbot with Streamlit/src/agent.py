
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


def extract_text(content):
    """Extract readable text from an AI message."""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []

        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    parts.append(block.get("text", ""))

        return "".join(parts)

    return str(content)


def ask_agent_with_tools(agent, question):
    """Run the agent and return its answer and executed tools."""

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": question}
        ]
    })

    messages = result["messages"]

    used_tools = []

    for message in messages:
        if getattr(message, "type", None) == "tool":
            tool_name = getattr(message, "name", None)

            if tool_name and tool_name not in used_tools:
                used_tools.append(tool_name)

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
        answer = extract_text(last_ai_message.content)

    return answer, used_tools


def stream_agent_response(agent, question, used_tools):
    """
    Stream actual AI response chunks from the agent.

    Tool execution happens as part of the agent workflow.
    Generated text is yielded progressively.
    """

    for chunk, metadata in agent.stream(
        {
            "messages": [
                {"role": "user", "content": question}
            ]
        },
        stream_mode="messages"
    ):

        # Record tool calls made by the AI
        tool_call_chunks = getattr(
            chunk, "tool_call_chunks", []
        ) or []

        for tool_call in tool_call_chunks:
            tool_name = tool_call.get("name")

            if tool_name and tool_name not in used_tools:
                used_tools.append(tool_name)

        # Ignore non-AI messages
        if getattr(chunk, "type", None) != "AIMessageChunk":
            continue

        # Ignore chunks that contain tool calls
        if tool_call_chunks:
            continue

        # Yield actual generated text
        text = extract_text(getattr(chunk, "content", ""))

        if text:
            yield text


def ask_agent(agent, question):
    """Return only the final answer for console usage."""

    answer, _ = ask_agent_with_tools(agent, question)
    return answer
