from blaze_data.market_cap import get_marketcap_data
from blaze_data.token_price import get_token_price
from blaze_data.Active_user import get_active_users_data



def get_blaze_data(chain,start_date,end_date):
    a=get_active_users_data(chain, start_date, end_date)
    b=get_token_price(chain, start_date, end_date)
    c=get_marketcap_data(chain, start_date, end_date)

    response = {
        "active_users-data": a,
        "token_price-data": b,
        "market_cap_data": c,
    }
    return response
