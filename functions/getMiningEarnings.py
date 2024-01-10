from functions.classes.APIService import APIService
from functions.classes.RPCProvider import RPCProvider
from functions.getPrices import getItemPriceJewel

miners_per_account = 18
avg_gold= 65 #per quest
tear_drop_rate = 0.1125 #per try
shvas_drop_rate = 0.015 #per try
moksha_drop_rate = 0.00045 #per try
egg_drop_rate = 0.0004 #per quest
loot_slots = 5

def getMiningEarnings(quest_per_day, apiService: APIService, rpcProvider: RPCProvider):
    tear_value = getItemPriceJewel("Gaias Tears", apiService, rpcProvider)
    gold_value = getItemPriceJewel("DFKGold", apiService, rpcProvider)
    shvas_value = getItemPriceJewel("Shvas Rune", apiService, rpcProvider)
    moksha_value = getItemPriceJewel("Moksha Rune", apiService, rpcProvider)
    egg_value = getItemPriceJewel("Yellow Pet Egg", apiService, rpcProvider)

    daily_gold = quest_per_day*avg_gold
    daily_gold_value = daily_gold*gold_value

    daily_tears = quest_per_day*loot_slots*tear_drop_rate
    daily_tears_value = daily_tears*tear_value

    daily_shvas = quest_per_day*loot_slots*shvas_drop_rate
    daily_shvas_value = daily_shvas*shvas_value

    daily_moksha = quest_per_day*loot_slots*moksha_drop_rate
    daily_moksha_value = daily_moksha*moksha_value

    daily_egg = quest_per_day*egg_drop_rate
    daily_egg_value = daily_egg*egg_value

    daily_income = daily_gold_value + daily_tears_value + daily_moksha_value + daily_shvas_value + daily_egg_value
    return daily_income*miners_per_account
