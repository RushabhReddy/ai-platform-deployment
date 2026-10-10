import streamlit as st
from openai import OpenAI
from groq import Groq
from google import genai
from core.config import config


def run_llm(provider, model_name, messages, max_tokens=500):
    if provider == "OpenAI":
        client = OpenAI(api_key=config.OPENAI_API_KEY)

    elif provider == "Groq":
        client = Groq(api_key=config.GROQ_API_KEY)

    else:
        client = genai.Client(api_key=config.GOOGLE_API_KEY)

    if provider == "Google":
        return client.models.generate_content(
            model=model_name,
            contents=[message["content"] for message in messages],
        ).text
    elif provider == "Groq":
        return (
            client.chat.completions.create(
                model=model_name, messages=messages, max_completion_tokens=max_tokens
            )
            .choices[0]
            .message.content
        )
    else:
        return (
            client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_completion_tokens=max_tokens,
                reasoning_effort="minimal",
            )
            .choices[0]
            .message.content
        )


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
        output = run_llm(
            st.session_state.provider,
            st.session_state.model_name,
            st.session_state.messages,
        )
        response_data = output
        answer = response_data
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
