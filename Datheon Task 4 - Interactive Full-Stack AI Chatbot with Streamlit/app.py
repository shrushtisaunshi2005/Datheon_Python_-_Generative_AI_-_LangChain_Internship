
import sys
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# --------------------------------------------------
# PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"

sys.path.insert(0, str(SRC_DIR))
load_dotenv(PROJECT_DIR / ".env")

from agent import build_agent, ask_agent_with_tools


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Chatbot - Task 4",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #4A90E2;
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


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🤖 Interactive AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Powered by LangChain and Google Gemini'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if "agent_error" not in st.session_state:
    st.session_state.agent_error = None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("⚙️ Chat Settings")

    st.subheader("Available AI Tools")

    st.write("🌐 Web Search")
    st.write("🧮 Calculator")
    st.write("📄 Local File Reader")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Task 4 - Datheon Internship")
    st.caption("Interactive Full-Stack AI Chatbot")


# --------------------------------------------------
# INITIALIZE AI AGENT
# --------------------------------------------------

if st.session_state.agent is None and st.session_state.agent_error is None:

    try:
        with st.spinner("Initializing AI Agent..."):
            st.session_state.agent = build_agent()

    except Exception as error:
        st.session_state.agent_error = str(error)


if st.session_state.agent_error:

    st.error(
        f"AI Agent initialization failed: "
        f"{st.session_state.agent_error}"
    )

    st.stop()


# --------------------------------------------------
# WELCOME MESSAGE
# --------------------------------------------------

if not st.session_state.messages:

    st.info(
        "👋 Hello! I am your AI assistant. "
        "Ask me questions, perform calculations, "
        "or search the web."
    )

    st.markdown("### Try these examples:")

    st.write("- Calculate 25% of 800.")
    st.write("- Search the web for LangChain.")
    st.write("- Read sample.txt and explain RAG.")


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            used_tools = message.get("tools", [])

            if used_tools:

                with st.expander("🔧 Tools Used"):

                    for tool_name in used_tools:
                        st.write(f"✅ {tool_name}")


# --------------------------------------------------
# CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input("Type your message here...")


# --------------------------------------------------
# PROCESS USER MESSAGE
# --------------------------------------------------

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    with st.chat_message("assistant"):

        try:

            # Build conversation context from previous messages
            previous_messages = st.session_state.messages[:-1]

            conversation_context = ""

            for message in previous_messages:

                role = message["role"].upper()
                content = message["content"]

                conversation_context += (
                    f"{role}: {content}\n"
                )

            # Include previous conversation in the current question
            contextual_question = f"""
You are a helpful AI assistant.

Use the previous conversation to understand follow-up questions.
Remember the information shared earlier in this conversation.

Previous conversation:
{conversation_context}

Current question:
{user_input}

Answer the current question clearly and naturally.
Use the available tools whenever necessary.
"""

            # Invoke AI agent
            with st.spinner("Thinking and selecting tools..."):

                answer, used_tools = ask_agent_with_tools(
                    st.session_state.agent,
                    contextual_question
                )

            # Stream response to the browser
            def response_stream():

                for word in answer.split(" "):

                    yield word + " "
                    time.sleep(0.025)

            st.write_stream(response_stream())

            # Display tools used
            if used_tools:

                with st.expander("🔧 Tools Used"):

                    for tool_name in used_tools:
                        st.write(f"✅ {tool_name}")

            # Save assistant response
            st.session_state.messages.append({

                "role": "assistant",
                "content": answer,
                "tools": used_tools

            })

        except Exception as error:

            error_message = (
                f"Sorry, something went wrong: {error}"
            )

            st.error(error_message)

            st.session_state.messages.append({

                "role": "assistant",
                "content": error_message,
                "tools": []

            })
