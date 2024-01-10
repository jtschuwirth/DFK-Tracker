import json

from functions.classes.APIService import APIService
from functions.classes.RPCProvider import RPCProvider
from functions.classes.Token import Token

RouterJson = open("abi/UniswapV2Router02.json")
RouterABI = json.load(RouterJson)



def getItemPriceJewel(item, apiService: APIService, rpcProvider: RPCProvider):
    RouterContract = rpcProvider.w3.eth.contract(address=apiService.contracts["Router"]["address"], abi=RouterABI)
    try:
        token: Token = apiService.tokens[item]
        price = RouterContract.functions.getAmountsOut(1, [token.address, apiService.tokens["Jewel"].address]).call()[1]
        price = price*(10**token.decimals)
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