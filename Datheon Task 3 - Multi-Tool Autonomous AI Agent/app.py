
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# -----------------------------------------
# PROJECT PATHS AND ENVIRONMENT CONFIGURATION
# -----------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"

# Add src folder before importing agent
sys.path.insert(0, str(SRC_DIR))

# Load Gemini API key
load_dotenv(PROJECT_DIR / ".env")

from agent import build_agent, ask_agent_with_tools


# -----------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------

st.set_page_config(
    page_title="Multi-Tool AI Agent",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------------------
# CUSTOM CSS
# -----------------------------------------

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    color: #4F8BF9;
}
.subtitle {
    text-align: center;
    color: gray;
    font-size: 16px;
}
.stChatMessage {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------
# HEADER
# -----------------------------------------

st.markdown(
    '<div class="main-title">🤖 Multi-Tool Autonomous AI Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Powered by LangChain and Google Gemini</div>',
    unsafe_allow_html=True
)

st.divider()


# -----------------------------------------
# TOOL DISPLAY NAMES
# -----------------------------------------

TOOL_LABELS = {
    "web_search": "🔎 DuckDuckGo Web Search",
    "calculator": "🧮 Python Calculator",
    "read_local_file": "📄 Local File Reader"
}


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:

    st.title("⚙️ Agent Dashboard")

    st.success("AI Agent Project")

    st.subheader("Available Tools")

    st.markdown("""
    🔎 **Web Search**

    Search the internet using DuckDuckGo.

    🧮 **Calculator**

    Perform mathematical calculations.

    📄 **Local File Reader**

    Read information from local documents.
    """)

    st.divider()

    st.subheader("Project Information")

    st.write("**Framework:** LangChain")
    st.write("**LLM:** Google Gemini")
    st.write("**Interface:** Streamlit")
    st.write("**Language:** Python")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# -----------------------------------------
# INITIALIZE SESSION STATE
# -----------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if "agent_error" not in st.session_state:
    st.session_state.agent_error = None


# -----------------------------------------
# BUILD AUTONOMOUS AI AGENT
# -----------------------------------------

if (
    st.session_state.agent is None
    and st.session_state.agent_error is None
):

    try:
        with st.spinner("Initializing AI Agent..."):
            st.session_state.agent = build_agent()

    except Exception as error:
        st.session_state.agent_error = str(error)


# -----------------------------------------
# AGENT STATUS
# -----------------------------------------

if st.session_state.agent:

    st.success("🟢 AI Agent is ready. Ask me anything!")

elif st.session_state.agent_error:

    st.error(
        f"Agent initialization failed: "
        f"{st.session_state.agent_error}"
    )


# -----------------------------------------
# WELCOME SECTION
# -----------------------------------------

if not st.session_state.messages:

    st.markdown("### 👋 Welcome!")

    st.write(
        "I am an autonomous AI assistant. "
        "I can search the web, perform calculations, "
        "and read your local documents."
    )

    st.markdown("### Try these example questions")

    st.markdown("""
    - 🔎 Search the web for information about LangChain.
    - 🧮 Calculate 25% of 800.
    - 📄 Read sample.txt and explain what Machine Learning means.
    - 🤖 Read sample.txt, calculate 15% of 240, and search for LangChain.
    """)


# -----------------------------------------
# DISPLAY TOOL EXECUTION HISTORY
# -----------------------------------------

def display_tool_history(used_tools):

    with st.expander("🔧 Tool Execution History"):

        if used_tools:

            for tool_name in used_tools:

                label = TOOL_LABELS.get(
                    tool_name,
                    tool_name
                )

                st.success(f"✓ {label} executed")

        else:

            st.info("No external tools were used.")


# -----------------------------------------
# DISPLAY PREVIOUS CHAT MESSAGES
# -----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            display_tool_history(
                message.get("tools", [])
            )


# -----------------------------------------
# CHAT INPUT
# -----------------------------------------

question = st.chat_input(
    "Ask your AI agent a question..."
)


# -----------------------------------------
# PROCESS USER QUESTION
# -----------------------------------------

if question:

    if st.session_state.agent is None:

        st.error(
            "The AI Agent is not available. "
            "Check your API key and restart."
        )

    else:

        # Display user question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Generate AI response
        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Agent is thinking and selecting tools..."
            ):

                try:

                    answer, used_tools = ask_agent_with_tools(
                        st.session_state.agent,
                        question
                    )

                    # Display answer
                    st.markdown(answer)

                    # Display actual tools used
                    display_tool_history(used_tools)

                    # Save assistant response and tool history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "tools": used_tools
                    })

                except Exception as error:

                    error_message = (
                        f"Something went wrong: {error}"
                    )

                    st.error(error_message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message,
                        "tools": []
                    })
