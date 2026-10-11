import streamlit as st
import requests
from chatbot_ui.core.config import config


def api_call(method, url, **kwargs):

    def _show_error_popup(message):
        """Show error message as a popup in the top-right corner."""
        st.session_state["error_popup"] = {
            "visible": True,
            "message": message,
        }

    try:
        response = getattr(requests, method)(url, **kwargs)

        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = {"message": "Invalid response format from server"}

        if response.ok:
            return True, response_data

        return False, response_data

    except requests.exceptions.ConnectionError:
        _show_error_popup("Connection error. Please check your network connection.")
        return False, {"message": "Connection error"}

    except requests.exceptions.Timeout:
        _show_error_popup("The request timed out. Please try again later.")
        return False, {"message": "Request timeout"}

    except Exception as e:
        _show_error_popup(f"An unexpected error occurred: {str(e)}")
        return False, {"message": str(e)}


## create a sidebar for selecting the LLM provider and model
with st.sidebar:
    st.title("Settings")
    # Dropdown to select the LLM provider and model
    provider = st.selectbox(
        "Select LLM Provider",
        ["OpenAI", "Groq", "Google"],
    )

    if provider == "OpenAI":
        model_name = st.selectbox(
            "Select OpenAI Model",
            ["gpt-5-nano"],
        )

    elif provider == "Groq":
        model_name = st.selectbox(
            "Select Groq Model",
            [
                "openai/gpt-oss-120b",
                "openai/gpt-oss-20b",
            ],
        )

    else:
        model_name = st.selectbox(
            "Select Google Model",
            [
                "gemini-3.8-flash",
                "gemini-3.5-flash",
            ],
        )
    # save provider and model_name in session state
    st.session_state["provider"] = provider
    st.session_state["model_name"] = model_name


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello, I am a helpful assistant."}
    ]

#
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Hello! How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        output = api_call(
            "post",
            f"{config.API_URL}/chat",
            json={
                "provider": st.session_state.provider,
                "models_name": st.session_state.model_name,
                "messages": st.session_state.messages,
            },
        )
        response_data = output[1]
        answer = response_data["message"]
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
