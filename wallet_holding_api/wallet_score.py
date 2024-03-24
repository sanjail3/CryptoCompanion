import requests
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY =os.getenv("BLAZEAI_API_KEY")

BLAZE_API_URL = "https://dashboard.withblaze.app/api/graphql-api"





QUERY = """
query WalletScores($walletAddress: String!){
    walletScores(walletAddress: $walletAddress){
        web3ReputationScore
        authenticityScore
    }
}
"""


def fetch_wallet_scores(wallet_address):

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }


    request_body = {"query": QUERY, "variables": {"walletAddress": wallet_address}}

    try:

        response = requests.post(BLAZE_API_URL, json=request_body, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        return response.json().get("data", {}).get("walletScores", {})
    except requests.exceptions.RequestException as e:
        print(f"Error executing GraphQL query: {e}")
        return None



def get_wallet_score(wallet_address):
    # wallet_address = "0x690B9A9E9aa1C9dB991C7721a92d351Db4FaC990"


    scores = fetch_wallet_scores(wallet_address)
    if scores:
        web3_reputation_score = scores.get("web3ReputationScore", None)
        authenticity_score = scores.get("authenticityScore", None)


        scores_dict = {
            "web3ReputationScore": web3_reputation_score,
            "authenticityScore": authenticity_score
        }


        print("Scores:", scores_dict)

        return scores_dict





