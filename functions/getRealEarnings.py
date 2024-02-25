from functions.classes.TablesManager import TablesManager

def getRealEarnings(tablesManager: TablesManager, profession, logger):
    payouts_list = tablesManager.payouts.scan()["Items"]
    total_earnings = 0
    total_time_delta = 0
    not_valids = 0
    for payout in payouts_list:
        payout_profession = payout["profession"]
        if payout_profession != profession:
            not_valids += 1
            continue
            
        if int(payout["time_delta"]) == 0:
            not_valids += 1
            continue

        total_earnings += float(payout["amount_"])
        total_time_delta += int(payout["time_delta"])
    avg_earnings = total_earnings/(len(payouts_list)-not_valids)
    avg_time_delta = total_time_delta/(len(payouts_list)-not_valids)
    avg_daily_earnings = avg_earnings/avg_time_delta*24*60*60
    return avg_daily_earnings
    

