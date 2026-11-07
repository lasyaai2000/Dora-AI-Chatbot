import json
import os
import time
import uuid

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

st.set_page_config(
    page_title="Dora AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-3.8-flash"


SYSTEM_PROMPT = """
You are Dora, a friendly, intelligent, helpful general-purpose AI assistant.

You can help with:
- General knowledge and explanations
- Programming and debugging
- Education and learning
- Writing and communication
- Business and creative ideas
- Technology and AI
- Mathematics and problem solving
- Career and productivity

Give accurate, clear and useful answers.
Explain complicated topics simply.
Use formatting and examples when helpful.
Be conversational, respectful and concise.
Never pretend to know something you do not know.
"""


# ==========================================
# GEMINI API CONNECTION
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

try:
    if not api_key:
        api_key = st.secrets.get("GEMINI_API_KEY")

except Exception:
    pass

client = None

if api_key:
    try:
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=45000)
        )

    except Exception as error:
        st.error(f"Gemini connection error: {error}")


# ==========================================
# COPY RESPONSE FUNCTION
# ==========================================

def render_copy_button(text):

    safe_text = json.dumps(
        text,
        ensure_ascii=False
    ).replace("</", "<\\/")

    html = f"""
    <html>
    <body style="margin:0;background:transparent;">

        <button id="copyBtn" style="
            background:#142744;
            color:#67E8F9;
            border:1px solid #304968;
            border-radius:9px;
            padding:7px 15px;
            font-size:12px;
            cursor:pointer;
        ">📋 Copy response</button>

        <script>
            const textToCopy = {safe_text};
            const button = document.getElementById("copyBtn");

            button.addEventListener("click", async () => {{
                try {{
                    await navigator.clipboard.writeText(textToCopy);
                    button.innerText = "✓ Copied!";
                }} catch (error) {{
                    try {{
                        const area = document.createElement("textarea");
                        area.value = textToCopy;
                        area.style.position = "fixed";
                        area.style.left = "-9999px";

                        document.body.appendChild(area);
                        area.select();

                        const copied = document.execCommand("copy");
                        area.remove();

                        button.innerText = copied
                            ? "✓ Copied!"
                            : "Copy failed";

                    }} catch (fallbackError) {{
                        button.innerText = "Copy failed";
                    }}
                }}
            }});
        </script>

    </body>
    </html>
    """

    components.html(
        html,
        height=42,
        scrolling=False
    )


# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>

/* MAIN APP */

.stApp {
    background: #070B16 !important;
    color: #F8FAFC !important;
}

.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp li {
    color: #F8FAFC;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #0B1220 !important;
    border-right: 1px solid #1E293B !important;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

/* MAIN TITLE */

.main-title {
    font-size: 48px;
    font-weight: 850;
    text-align: center;
    margin-top: 35px;
    color: #FFFFFF !important;
    letter-spacing: -2px;
}

.gradient-text {
    background: linear-gradient(90deg, #67E8F9, #818CF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #B8C5D8 !important;
    font-size: 16px;
    margin-bottom: 45px;
}

.section-title {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #A5B4FC !important;
    margin-bottom: 15px;
}

/* FEATURE CARDS */

.feature-card {
    background: linear-gradient(135deg, #14213A, #10182B);
    border: 1px solid #293B5B;
    border-radius: 16px;
    padding: 22px;
    min-height: 110px;
    margin-bottom: 12px;
    color: #E2E8F0 !important;
}

.feature-card b {
    color: #FFFFFF !important;
}

/* CHAT MESSAGE CARDS */

[data-testid="stChatMessage"] {
    background: #111D33 !important;
    border: 1px solid #304563 !important;
    border-radius: 18px !important;
    padding: 18px !important;
    margin-bottom: 18px !important;
}

/* CHAT TEXT */

[data-testid="stChatMessage"] *,
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    opacity: 1 !important;
    line-height: 1.75 !important;
}

/* CHAT LINKS */

[data-testid="stChatMessage"] a {
    color: #67E8F9 !important;
    -webkit-text-fill-color: #67E8F9 !important;
}

/* CHAT CODE */

[data-testid="stChatMessage"] pre {
    background: #080F1C !important;
    border: 1px solid #304563 !important;
    border-radius: 12px !important;
    padding: 14px !important;
}

[data-testid="stChatMessage"] code {
    color: #93C5FD !important;
    -webkit-text-fill-color: #93C5FD !important;
    background: #172338 !important;
}

/* CHAT INPUT */

[data-testid="stChatInput"] {
    background: #111D33 !important;
    border: 1.5px solid #4775B8 !important;
    border-radius: 18px !important;
    padding: 5px 8px !important;
    box-shadow: 0 0 22px rgba(59, 130, 246, 0.16) !important;
}

[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div,
[data-testid="stChatInput"] textarea {
    background-color: #111D33 !important;
}

/* TYPED TEXT */

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea:focus {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    caret-color: #67E8F9 !important;
    font-size: 15px !important;
    font-weight: 500 !important;
    opacity: 1 !important;
}

/* PLACEHOLDER */

[data-testid="stChatInput"] textarea::placeholder {
    color: #B8C5D8 !important;
    -webkit-text-fill-color: #B8C5D8 !important;
    opacity: 1 !important;
}

/* SEND BUTTON */

[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #FFFFFF !important;
}

[data-testid="stChatInput"] button svg {
    color: #FFFFFF !important;
    fill: #FFFFFF !important;
}

/* BOTTOM AREA */

[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background: #070B16 !important;
}

/* OTHER BUTTONS */

.stButton button {
    background: #142744 !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #304968 !important;
    border-radius: 12px !important;
    transition: 0.2s;
}

.stButton button:hover {
    background: #243D63 !important;
    border-color: #67E8F9 !important;
    color: #FFFFFF !important;
}

/* STATUS */

.status-box {
    background: #111D33;
    border: 1px solid #263957;
    border-radius: 12px;
    padding: 12px;
    color: #CBD5E1 !important;
    font-size: 13px;
}

/* ALERTS */

[data-testid="stAlert"] {
    background: #172338 !important;
    color: #FFFFFF !important;
}

[data-testid="stAlert"] * {
    color: #FFFFFF !important;
}

/* DIVIDERS */

hr {
    border-color: #263957 !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# PRIVATE SESSION CHAT STORAGE
# ==========================================

# IMPORTANT:
# Each visitor gets their own Streamlit session.
# Conversations are stored ONLY in that session.
# No shared JSON file or global chat history.

if "chats" not in st.session_state:

    chat_id = str(uuid.uuid4())

    st.session_state.chats = {
        chat_id: []
    }

    st.session_state.active_chat = chat_id


if "active_chat" not in st.session_state:
    st.session_state.active_chat = next(
        iter(st.session_state.chats)
    )


if (
    st.session_state.active_chat
    not in st.session_state.chats
):

    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = []
    st.session_state.active_chat = chat_id


messages = st.session_state.chats[
    st.session_state.active_chat
]


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown(
        '<div class="main-title" style="font-size:34px;'
        'text-align:left;margin-top:5px;">'
        '<span class="gradient-text">DORA.</span></div>',
        unsafe_allow_html=True
    )

    st.caption("Your independent AI companion")

    st.markdown("---")

    # NEW CONVERSATION

    if st.button(
        "＋  New conversation",
        use_container_width=True
    ):

        chat_id = str(uuid.uuid4())

        st.session_state.chats[chat_id] = []
        st.session_state.active_chat = chat_id

        st.rerun()

    # CONVERSATION HISTORY

    st.markdown("### Your conversations")

    for chat_id, chat_messages in reversed(
        list(st.session_state.chats.items())
    ):

        if chat_messages:

            title = chat_messages[0]["content"][:25]

        else:

            title = "New conversation"

        if st.button(
            "◈  " + title,
            key=chat_id,
            use_container_width=True
        ):

            st.session_state.active_chat = chat_id

            st.rerun()

    st.markdown("---")

    # GEMINI STATUS

    if client:

        st.markdown(
            '<div class="status-box">'
            '● Gemini connection initialized'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="status-box">'
            '● API key not detected'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.caption("DORA AI")
    st.caption("Think. Explore. Create.")

    # CLEAR CURRENT CONVERSATION

    if st.button(
        "Clear current conversation",
        use_container_width=True
    ):

        st.session_state.chats[
            st.session_state.active_chat
        ] = []

        st.rerun()


# ==========================================
# MAIN HEADER
# ==========================================

st.markdown(
    '<div class="main-title">Meet '
    '<span class="gradient-text">DORA.</span></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Think. Explore. Create. Ask anything.'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# WELCOME SCREEN
# ==========================================

if not messages:

    st.markdown(
        '<div class="section-title">'
        'TRY ASKING DORA'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Explain artificial intelligence simply",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Explain artificial intelligence simply"
            )

            st.rerun()

        if st.button(
            "Give me a creative business idea",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Give me a creative business idea"
            )

            st.rerun()

    with col2:

        if st.button(
            "Write a Python program to reverse a string",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Write a Python program to reverse a string"
            )

            st.rerun()

        if st.button(
            "Help me prepare for a technical interview",
            use_container_width=True
        ):

            st.session_state.pending_prompt = (
                "Help me prepare for a technical interview"
            )

            st.rerun()


# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in messages:

    with st.chat_message(
        "assistant"
        if message["role"] == "assistant"
        else "user"
    ):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            render_copy_button(message["content"])


# ==========================================
# AI RESPONSE FUNCTION
# ==========================================

def ask_dora(conversation):

    models_to_try = [
        MODEL,
        FALLBACK_MODEL
    ]

    last_error = None

    for selected_model in models_to_try:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=selected_model,
                    contents=conversation,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.7,
                        max_output_tokens=2048
                    )
                )

                answer = response.text

                if answer and answer.strip():

                    return answer

                raise ValueError(
                    "The model returned an empty response."
                )

            except Exception as error:

                last_error = error

                error_text = str(error).lower()

                retryable = (
                    "503" in error_text
                    or "429" in error_text
                    or "500" in error_text
                    or "unavailable" in error_text
                    or "overloaded" in error_text
                    or "timeout" in error_text
                )

                if retryable and attempt == 0:

                    time.sleep(2)

                    continue

                break

    raise RuntimeError(
        f"Both Gemini model attempts failed. "
        f"Last error: {last_error}"
    )


# ==========================================
# CHAT INPUT AND PROCESSING
# ==========================================

prompt = st.chat_input("Message Dora...")

if "pending_prompt" in st.session_state:

    prompt = st.session_state.pop("pending_prompt")


if prompt:

    response_text = ""

    # SAVE USER MESSAGE IN THIS SESSION ONLY

    messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):

        st.markdown(prompt)

    # DORA RESPONSE

    with st.chat_message("assistant"):

        if not client:

            response_text = (
                "Dora cannot connect because the API key "
                "was not detected. Please check your "
                "Streamlit Secrets or local .env file."
            )

            st.error(response_text)

        else:

            with st.spinner("Dora is thinking..."):

                conversation = []

                for message in messages:

                    conversation.append({
                        "role": (
                            "model"
                            if message["role"] == "assistant"
                            else "user"
                        ),
                        "parts": [
                            {"text": message["content"]}
                        ]
                    })

                try:

                    response_text = ask_dora(conversation)

                    st.markdown(response_text)

                except Exception as error:

                    response_text = (
                        "I couldn't generate a response.\n\n"
                        f"**Technical detail:** "
                        f"{type(error).__name__}: {error}"
                    )

                    st.error(response_text)

        # COPY BUTTON

        if response_text:

            render_copy_button(response_text)

    # SAVE ASSISTANT MESSAGE IN THIS SESSION ONLY

    messages.append({
        "role": "assistant",
        "content": response_text
    })

    st.rerun()