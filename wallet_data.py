from wallet_holding_api.wallet_holding import get_walletportfolio
from wallet_holding_api.wallet_portfolio import get_chain_data
from wallet_holding_api.wallet_score import get_wallet_score
from wallet_holding_api.social_handle import get_socialmedia_handle



def get_all_data(wallet):
    a=get_walletportfolio(wallet)
    b=get_chain_data(wallet)
    c=get_wallet_score(wallet)
    d=get_socialmedia_handle(wallet)


    response={
        "Wallet-portfolio-data":a,
        "Chain-holding-data":b,
        "Wallet-scoring-data":c,
        "Social-media-detail":d
    }
    return response



