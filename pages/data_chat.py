import streamlit as st
from openai import OpenAI
from blaze_data_api import get_blaze_data
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
avatar_img = "static\Crypto-Companion-L-avatar.png"
st.set_page_config(
    page_title="Ask CryptoCompanion", page_icon=avatar_img)


def get_user_inputs():
    if "user_inputs" not in st.session_state:
        with st.sidebar:
            st.subheader("Enter Details")
            wallet_chain = st.selectbox("Select Blockchain", ["ETHEREUM", "ARBITRUM", "BSC", "OPTIMISM", "BASE", "POLYGON"])
            start_date = st.date_input("Start Date", min_value=None, max_value=None, value=None, key=None)
            end_date = st.date_input("End Date", min_value=None, max_value=None, value=None, key=None)

            print(wallet_chain,start_date,end_date)
            if st.button("Submit"):
                st.session_state.user_inputs = {"chain": wallet_chain, "start_date": str(start_date), "end_date": str(end_date)}
                st.success("✅ Inputs submitted!")
                return st.session_state.user_inputs
    else:
        return st.session_state.user_inputs


def ask_and_respond(prompt, chain_data):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    encoded_prompt = f"Chain Data: {chain_data}  based on input parameters try to answer this query {prompt}"

    print(encoded_prompt)

    with st.chat_message("assistant", avatar=avatar_img):
        with st.spinner('Processing...'):
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": encoded_prompt}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    user_inputs = get_user_inputs()
    if user_inputs is None:
        st.error("Please enter the details for chatting.")
        return

    if user_inputs and "blaze_data" not in st.session_state:

        st.session_state.blaze_data = get_blaze_data(user_inputs['chain'], user_inputs['start_date'], user_inputs['end_date'])



    start_message = st.chat_message("assistant", avatar=avatar_img)
    start_message.write("Hello there, what questions about Crypto can I help you with today?")
    start_message.write("Examples of questions I can answer:")
    examples = [
        "Brief About the Market Trends",
        "Explain about the  Projected growth",
        "Can I make some investment based on the trends ",
        "What inference I can make ",
    ]
    example_buttons = [start_message.button(example) for example in examples]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    for example, example_button in zip(examples, example_buttons):
        if example_button:
            ask_and_respond(example, st.session_state.blaze_data)

    chat_input_box = st.chat_input("What would you like to ask about?")
    if chat_input_box:
        ask_and_respond(chat_input_box, st.session_state.blaze_data)


if __name__ == "__main__":
    main()
