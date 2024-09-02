from dfk_commons.classes.TablesManager import TablesManager
from boto3.dynamodb.conditions import Attr
import time

def getRealEarnings(tablesManager: TablesManager, profession):
    payouts_list = tablesManager.payouts.scan(
         FilterExpression=Attr('profession').eq(profession)
    )["Items"]
    total_earnings = 0
    total_time_delta = 0
    not_valids = 0
    for payout in payouts_list:        
        if int(payout["time_delta"]) == 0:
            not_valids += 1
            continue

        if int(payout["time_"]) < (int(time.time()) - 7*24*60*60):
            not_valids += 1
            continue


        total_earnings += float(payout["amount_"])
        total_time_delta += int(payout["time_delta"])
    avg_earnings = total_earnings/(len(payouts_list)-not_valids)
    avg_time_delta = total_time_delta/(len(payouts_list)-not_valids)
    avg_daily_earnings = avg_earnings/avg_time_delta*24*60*60
    return avg_daily_earnings
    

