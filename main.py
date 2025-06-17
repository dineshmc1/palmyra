import streamlit as st
from openai import OpenAI

import io
import PyPDF2

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=""
)

st.title("Palmyra Financial Report Analyzer")

# File uploader for financial report
uploaded_file = st.file_uploader("Upload a company's financial report (PDF or TXT)", type=["pdf", "txt"])

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        report_text = ""
        for page in pdf_reader.pages:
            report_text += page.extract_text() or ""
    else:
        report_text = uploaded_file.read().decode("utf-8")

    st.subheader("Extracted Report Text (first 1000 chars):")
    st.write(report_text[:1000] + ("..." if len(report_text) > 1000 else ""))

    if st.button("Analyze Report"):
        with st.spinner("Analyzing report with AI..."):
            system_prompt = (
                "You are a financial analyst AI. Analyze the following company's financial report and provide a summary of the company's performance, highlighting strengths, weaknesses, and any notable trends."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": report_text}
            ]
            response_placeholder = st.empty()
            ai_response = ""
            completion = client.chat.completions.create(
                model="writer/palmyra-fin-70b-32k",
                messages=messages,
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
                stream=True
            )
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    ai_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(f"**AI Analysis:** {ai_response}")
            st.session_state["analysis"] = ai_response

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "analysis" not in st.session_state:
    st.session_state["analysis"] = None

if st.session_state["analysis"]:
    st.subheader("Chat with AI about the report")
    # Display chat history
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")
    # User input
    user_input = st.text_input("You:", "", key="input")
    if st.button("Send") and user_input.strip():
        st.session_state["messages"].append({"role": "user", "content": user_input})
        # Add the analysis as context for the AI
        messages = [
            {"role": "system", "content": "You are a financial analyst AI. Use the following analysis as context: " + st.session_state["analysis"]},
        ] + st.session_state["messages"]
        response_placeholder = st.empty()
        ai_response = ""
        completion = client.chat.completions.create(
            model="writer/palmyra-fin-70b-32k",
            messages=messages,
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                ai_response += chunk.choices[0].delta.content
                response_placeholder.markdown(f"**AI:** {ai_response}")
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})

