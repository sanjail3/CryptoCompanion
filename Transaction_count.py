import requests



def get_active_users(chain, start_date, end_date):
    # Endpoint URL
    url = "https://dashboard.withblaze.app/api/chain-insights/transaction_count"

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
        transaction_count = response.json()
        return {"status": "success", "data": transaction_count}

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching token prices: {e}"
        print(error_message)
        return {"status": "error", "message": error_message}


def get_transaction_count_data(chain,start_date,end_date):
    chain = "ETHEREUM"
    start_date = "2023-01-01"
    end_date = "2023-01-07"

    response = get_active_users(chain, start_date, end_date)
    if response["status"] == "success":
        transaction_count= response["data"]
        transaction_count_dict = {price['date']: price['active_users'] for price in  transaction_count}
        print("Token Prices Dictionary:")
        print( transaction_count_dict)

        return  transaction_count_dict
    else:
        print("Failed to fetch token prices.")


get_transaction_count_data("","","")
