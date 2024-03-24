import streamlit as st
from openai import OpenAI
from wallet_data import get_all_data
from dotenv import load_dotenv

load_dotenv()
import os
api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

avatar_img = "static/Crypto-Companion-L-avatar.png"
st.set_page_config(
    page_title="Ask CryptoCompanion", page_icon=avatar_img)




def get_wallet_from_user():
    if "wallet" not in st.session_state:
        with st.sidebar:
            st.subheader("Enter the Wallet Address")
            wallet_address = st.text_input("Wallet Address", type="password")
            if st.button("Add"):
                st.session_state.wallet = wallet_address
                st.success("✅ Wallet added!")
                return wallet_address
    else:
        return st.session_state.wallet









def ask_and_respond(prompt,wallet_data):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    encoded_prompt = f"WalletData: {wallet_data}  based on wallet holding data try to answer this query {prompt}"

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







    # st.session_state.messages.append(
    #     {"role": "assistant", "content": ""})








def main():

    wallet = get_wallet_from_user()
    if wallet is None:
        st.error("Please enter the wallet address for chatting.")
        return

    if wallet and "wallet_data" not in st.session_state:

        st.session_state.wallet_data = get_all_data(wallet)



    # wallet_data = get_all_data(wallet)  # Define get_all_data(wallet) function appropriately


    start_message = st.chat_message("assistant",avatar=avatar_img)
    start_message.write("Hello there, what questions about Crypto can I help you with today?")
    start_message.write("Examples of questions I can answer:")
    examples = [
        "Brief About this wallet portfolio ",
        "Explain the wallet holding details",
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
            ask_and_respond(example, st.session_state.wallet_data )

    chat_input_box = st.chat_input("What would you like to ask about?")
    if chat_input_box:
        ask_and_respond(chat_input_box, st.session_state.wallet_data )

if __name__ == "__main__":
    main()

