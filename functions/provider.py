from web3 import Web3
from dotenv import load_dotenv
load_dotenv()
from web3.middleware import geth_poa_middleware

def get_provider(network):
    if network == "dfk":
        rpc_url = "https://subnets.avax.network/defi-kingdoms/dfk-chain/rpc"
    elif network== "kla":
        rpc_url = "https://public-en-cypress.klaytn.net"
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    w3.clientVersion
    return w3
