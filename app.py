import streamlit as st
import ollama
from groq import Groq

st.set_page_config(
    page_title="AI Personal Finance Coach",
    page_icon="💰"
)

st.title("💰 AI Personal Finance Coach")

# Language Selection
language = st.selectbox(
    "Select Language",
    ["English", "Hindi", "Telugu", "Tamil", "Kannada"]
)

# AI Mode Selection
ai_mode = st.radio(
    "Choose AI Mode",
    ["Local AI (Ollama)", "BYOK (Groq)"]
)

# API Key Input
api_key = ""

if ai_mode == "BYOK (Groq)":
    api_key = st.text_input(
        "Enter Groq API Key",
        type="password"
    )

st.header("📊 Monthly Budget Details")

income = st.number_input(
    "Monthly Income (₹)",
    min_value=0
)

rent = st.number_input(
    "Rent (₹)",
    min_value=0
)

food = st.number_input(
    "Food Expenses (₹)",
    min_value=0
)

transport = st.number_input(
    "Transport Expenses (₹)",
    min_value=0
)

other = st.number_input(
    "Other Expenses (₹)",
    min_value=0
)

# Budget Analysis
if st.button("Analyze Budget"):

    total_expenses = rent + food + transport + other
    savings = income - total_expenses

    st.subheader("📈 Financial Summary")

    st.write(f"**Monthly Income:** ₹{income}")
    st.write(f"**Total Expenses:** ₹{total_expenses}")
    st.write(f"**Potential Savings:** ₹{savings}")

    prompt = f"""
    Respond completely in {language}.

    Monthly Income: {income}
    Total Expenses: {total_expenses}
    Savings: {savings}

    Give:
    1. Budget Analysis
    2. Saving Tips
    3. Financial Recommendations
    4. Areas where expenses can be reduced
    """

    try:

        if ai_mode == "Local AI (Ollama)":

            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response["message"]["content"]

        else:

            if not api_key:
                st.warning("Please enter your Groq API Key.")
                st.stop()

            client = Groq(api_key=api_key)

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content

        st.subheader("🤖 AI Financial Advice")
        st.write(result)

    except Exception as e:
        st.error(str(e))

# --------------------------
# Finance Chatbot
# --------------------------

st.divider()

st.header("💬 Ask Finance Questions")

question = st.text_input(
    "Ask anything about budgeting, saving, investing, or finance"
)

if st.button("Ask AI"):

    if question.strip():

        prompt = f"""
        Respond completely in {language}.

        User Question:
        {question}
        """

        try:

            if ai_mode == "Local AI (Ollama)":

                response = ollama.chat(
                    model="llama3",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response["message"]["content"]

            else:

                if not api_key:
                    st.warning("Please enter your Groq API Key.")
                    st.stop()

                client = Groq(api_key=api_key)

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                answer = response.choices[0].message.content

            st.subheader("🤖 AI Answer")
            st.write(answer)

        except Exception as e:
            st.error(str(e))