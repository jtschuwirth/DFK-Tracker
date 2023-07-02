import json

itemsJson = open("items_data/items_dfkchain.json")
items = json.load(itemsJson)

decimalsJson = open("items_data/decimals.json")
decimals_data = json.load(decimalsJson)

RouterAddress = "0x3C351E1afdd1b1BC44e931E12D4E05D6125eaeCa"
RouterJson = open("abi/UniswapV2Router02.json")
RouterABI = json.load(RouterJson)



def getItemPriceJewel(item, w3):
    RouterContract = w3.eth.contract(address=RouterAddress, abi=RouterABI)
    try:
        decimals = 0
        if item in decimals_data:
            decimals = decimals_data[item]
        price = RouterContract.functions.getAmountsOut(1, [items[item], items["Jewel"]]).call()[1]
        price = price*(10**decimals)
    except Exception as e:
        print(e)
        price = 0
    return price

def getCrystalPriceJewel(w3):
    RouterContract = w3.eth.contract(address=RouterAddress, abi=RouterABI)
    try:
        price = RouterContract.functions.getAmountsOut(1*10**18, [items["Crystal"], items["Jewel"]]).call()[1]
        price = price
    except Exception as e:
        print(e)
        price = 0
    return price