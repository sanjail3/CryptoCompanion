import requests
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY =os.getenv("BLAZEAI_API_KEY")

# GraphQL endpoint
BLAZE_API_URL = "https://dashboard.withblaze.app/api/graphql-api"

# Your API key


# GraphQL query
QUERY = """
query WalletHoldings($walletAddress: String!){
    walletHoldings(walletAddress: $walletAddress){
        walletAddress
        erc20Tokens{
            chain
            tokenAddress
            tokenName
            tokenSymbol
        }
        erc721Tokens{
            chain
            tokenAddress
            tokenName
            tokenSymbol
        }
        erc1155Tokens{
            chain
            tokenAddress
            tokenName
            tokenSymbol
        }
    }
}
"""
def parse_and_store_tokens(wallet_holdings):
    erc20_tokens = wallet_holdings.get("erc20Tokens", [])
    erc721_tokens = wallet_holdings.get("erc721Tokens", [])
    erc1155_tokens = wallet_holdings.get("erc1155Tokens", [])

    token_count = {}

    # Count ERC20 tokens
    for token in erc20_tokens:
        token_address = token.get("chain")
        if token_address in token_count:
            token_count[token_address] += 1
        else:
            token_count[token_address] = 1

    # Count ERC721 tokens
    for token in erc721_tokens:
        token_address = token.get("chain")
        if token_address in token_count:
            token_count[token_address] += 1
        else:
            token_count[token_address] = 1

    # Count ERC1155 tokens
    for token in erc1155_tokens:
        token_address = token.get("chain")
        if token_address in token_count:
            token_count[token_address] += 1
        else:
            token_count[token_address] = 1

    # Store token data based on count and number
    token_data = {}
    for token_address, count in token_count.items():
        token_data[token_address] = {
            "count": count,
            "number": token_address[-4:]  # Extract last 4 characters of token address as number
        }

    return token_data

def fetch_data_for_wallet(wallet_address,API_KEY):
    # GraphQL request headers with API key
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': API_KEY
    }

    # GraphQL request body
    request_body = {"query": QUERY, "variables": {"walletAddress": wallet_address}}

    try:
        # Send GraphQL request
        response = requests.post(BLAZE_API_URL, json=request_body, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        return response.json().get("data", {}).get("walletHoldings", {})
    except requests.exceptions.RequestException as e:
        print(f"Error executing GraphQL query: {e}")
        return None

# Example usag

def get_chain_data(wallet_address):
    # wallet_address = "0x690B9A9E9aa1C9dB991C7721a92d351Db4FaC990"

    # Fetch data for the wallet address
    wallet_holdings = fetch_data_for_wallet(wallet_address, API_KEY)

    token_data = parse_and_store_tokens(wallet_holdings)
    
    chain_holding = {}
    for token_name, data in token_data.items():
        chain_holding[token_name] = data['count']
        print(f"Chain: {token_name}, Count: {data['count']}")

   

