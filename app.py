import streamlit as st
import base64
from streamlit_card import card
import streamlit.components.v1 as components








def get_image_data(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data








st.set_page_config(page_title="CryptoComapanion", page_icon="🪙", layout="centered")


def main():
    # show logo image in center

    _, img_col, _ = st.columns([1, 3, 1])
    img_col.image("static/Crypto-Companion-Logo.png")

    st.info(
        """
        **Welcome to CryptoCompanion** 🚀

        This Project answers any questions related to your Wallet and also finds market trends
        and answers any answer related to crypto
        """
    )

    with st.sidebar:
        _, img_col, _ = st.columns([1, 3, 1])
        img_col.image("static/Crypto-Companion-Logo.png")
    st.markdown("--- ")
    st.header("🛠️ Tools")
    col1, col2 = st.columns(2)

    video_image_1 = get_image_data("static/Crypto-Companion-Logo.png")

    with col1:
        hasClicked = card(
            title="🪙Wallet-Chat",
            text="",
            image=video_image_1,
            url="/wallet_chat",
            key="image_card1",
            styles={
                "card": {
                    "width": "100%",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.8)"  # <- make the image not dimmed anymore
                },
            },
        )
    with col2:
        hasClicked = card(
            title="💹 Chain-Chat",
            text="",
            image=video_image_1,
            url="/data_chat",
            key="image_card",
            styles={
                "card": {
                    "width": "100%",
                },
                "filter": {
                    "background-color": "rgba(0, 0, 0, 0.8)"  # <- make the image not dimmed anymore
                },
            },
        )











if __name__ == "__main__":

    main()

