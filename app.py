import streamlit as st
import requests
import uuid

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="GCB HR Connect",
    page_icon="⚡",
    layout="wide"
)

# ----------------------------
# Session State
# ----------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# Header
# ----------------------------
st.title("GCB HR Connect")
st.caption("Ask any HR policy related question")

# ----------------------------
# Display Chat History
# ----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------
# User Input
# ----------------------------
prompt = st.chat_input("Ask me anything about your workplace...")

if prompt:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    "https://n8n.gcbservicesit.com/webhook/hr-bot",
                    json={
                        "sessionId": st.session_state.session_id,
                        "chatInput": prompt
                    },
                    timeout=120
                )

                response.raise_for_status()

                if not response.text.strip():
                    answer = "Sorry, I couldn't get a response from the server."
                else:
                    data = response.json()

                    answer = (
                        data.get("output")
                        or data.get("response")
                        or data.get("answer")
                        or "No response received."
                    )

            except requests.exceptions.Timeout:
                answer = "⏱️ The request timed out. Please try again."

            except requests.exceptions.ConnectionError:
                answer = "🌐 Unable to connect to the chatbot service."

            except requests.exceptions.HTTPError as e:
                answer = f"⚠️ Server Error ({response.status_code})"

            except Exception:
                answer = "❌ Something went wrong. Please try again."

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )
