from functions.getPrices import getItemPriceJewel
from dfk_commons.classes.APIService import APIService
from dfk_commons.classes.RPCProvider import RPCProvider

heroes_per_account = 18
tear_drop_rate = 0.1125 #per try
shvas_drop_rate = 0.015 #per try
moksha_drop_rate = 0.00045 #per try
blue_stem_drop_rate = 0.09 #per try
spiderfruit_drop_rate = 0.06 #per try
milkweed_drop_rate = 0.04 #per try
egg_drop_rate = 0.005*2/100 #per quest
loot_slots = 5

def getGardeningEarnings(quest_per_day, apiService: APIService, rpcProvider: RPCProvider, logger):
    tear_value = getItemPriceJewel("Gaias Tears", apiService, rpcProvider)

    shvas_value = getItemPriceJewel("Shvas Rune", apiService, rpcProvider)
    moksha_value = getItemPriceJewel("Moksha Rune", apiService, rpcProvider)

    gold_value = getItemPriceJewel("DFKGold", apiService, rpcProvider)

    blue_stem_value = gold_value*5
    spiderfruit_value = gold_value*10
    milkweed_value = gold_value*12.5

    egg_value = getItemPriceJewel("Green Pet Egg", apiService, rpcProvider)

    crystal_value = getItemPriceJewel("Crystal", apiService, rpcProvider)

    daily_tears = quest_per_day*loot_slots*tear_drop_rate
    daily_tears_value = daily_tears*tear_value

    daily_shvas = quest_per_day*loot_slots*shvas_drop_rate
    daily_shvas_value = daily_shvas*shvas_value

    daily_moksha = quest_per_day*loot_slots*moksha_drop_rate
    daily_moksha_value = daily_moksha*moksha_value

    daily_blue_stem = quest_per_day*loot_slots*blue_stem_drop_rate
    daily_blue_stem_value = daily_blue_stem*blue_stem_value

    daily_spiderfruit = quest_per_day*loot_slots*spiderfruit_drop_rate
    daily_spiderfruit_value = daily_spiderfruit*spiderfruit_value

    daily_milkweed = quest_per_day*loot_slots*milkweed_drop_rate
    daily_milkweed_value = daily_milkweed*milkweed_value

    daily_egg = quest_per_day*egg_drop_rate
    daily_egg_value = daily_egg*egg_value

    daily_jewel_reward = (quest_per_day/2)*0.005*10**18

    daily_crystal_reward = (quest_per_day/2)*0.005 + 0.099*(quest_per_day/2)*0.1 + 0.001*(quest_per_day/2)*1
    daily_crystal_value = daily_crystal_reward*crystal_value

    daily_income = daily_jewel_reward + daily_crystal_value + daily_tears_value + daily_moksha_value + daily_shvas_value + daily_egg_value + daily_blue_stem_value + daily_spiderfruit_value + daily_milkweed_value
    return daily_income*heroes_per_account
