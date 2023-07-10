from functions.getPrices import getItemPriceJewel

from functions.provider import get_provider
from functions.initTables import initPayoutsTable

w3 = get_provider("dfk")

def getRealEarnings():
    payouts_table = initPayoutsTable()
    payouts_list = payouts_table.scan()["Items"]
    total_earnings = 0
    total_time_delta = 0
    no_stats = 0
    for payout in payouts_list:
        if int(payout["time_delta"]) == 0:
            no_stats += 1
            continue
        total_earnings += float(payout["amount_"])
        total_time_delta += int(payout["time_delta"])
    avg_earnings = total_earnings/(len(payouts_list)-no_stats)
    avg_time_delta = total_time_delta/(len(payouts_list)-no_stats)
    avg_daily_earnings = avg_earnings/avg_time_delta*24*60*60
    return avg_daily_earnings
    

