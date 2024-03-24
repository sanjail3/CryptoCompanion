import requests

from dotenv import load_dotenv
load_dotenv()
import os
API_KEY =os.getenv("BLAZEAI_API_KEY")

def get_active_users(chain, start_date, end_date):
    # Endpoint URL
    url = "https://dashboard.withblaze.app/api/chain-insights/active_users"

    # Request headers
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    # Request body
    payload = {
        "chain": chain,
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        # Send POST request with JSON payload
        response = requests.get(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes

        # Parse JSON response
        active_users = response.json()
        return {"status": "success", "data": active_users}

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching token prices: {e}"
        print(error_message)
        return {"status": "error", "message": error_message}


def get_active_users_data(chain,start_date,end_date):


    response = get_active_users(chain, start_date, end_date)
    if response["status"] == "success":
        active_users= response["data"]
        active_users_dict = {price['date']: price['active_users'] for price in  active_users}
        print("Token Prices Dictionary:")
        print( active_users_dict)

        return  active_users_dict
    else:
        print("Failed to fetch token prices.")


get_active_users_data("","","")