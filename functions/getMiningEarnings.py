from functions.getPrices import getItemPriceJewel

from functions.provider import get_provider

w3 = get_provider("dfk")

miners_per_account = 18
heros_per_quest = 6
avg_gold= 65 #per quest
tear_drop_rate = 0.1125 #per try
shvas_drop_rate = 0.015 #per try
moksha_drop_rate = 0.00045 #per try
egg_drop_rate = 0.0004 #per quest
loot_slots = 5

def getMiningEarnings(quest_per_day):
    tear_value = getItemPriceJewel("Gaias Tears", w3)
    gold_value = getItemPriceJewel("DFKGold", w3)
    shvas_value = getItemPriceJewel("Shvas Rune", w3)
    moksha_value = getItemPriceJewel("Moksha Rune", w3)
    egg_value = getItemPriceJewel("Yellow Pet Egg", w3)

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
