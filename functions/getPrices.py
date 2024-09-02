from dfk_commons.classes.APIService import APIService
from dfk_commons.classes.RPCProvider import RPCProvider
from dfk_commons.classes.Token import Token
from dfk_commons.abi_getters import RouterABI



def getItemPriceJewel(item, apiService: APIService, rpcProvider: RPCProvider):
    RouterContract = rpcProvider.w3.eth.contract(address=apiService.contracts["Router"]["address"], abi=RouterABI)
    try:
        token: Token = apiService.tokens[item]
        price = RouterContract.functions.getAmountsOut(1*(10**token.decimals), [token.address, apiService.tokens["Jewel"].address]).call()[1]
        price = price
    except Exception as e:
        print(e)
        price = 0
    return price

def getCrystalPriceJewel(apiService: APIService, rpcProvider: RPCProvider):
    RouterContract = rpcProvider.w3.eth.contract(address=apiService.contracts["Router"]["address"], abi=RouterABI)
    try:
        price = RouterContract.functions.getAmountsOut(1*10**18, [apiService.tokens["Crystal"].address, apiService.tokens["Jewel"].address]).call()[1]
        price = price
    except Exception as e:
        print(e)
        price = 0
    return price