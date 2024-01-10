from functions.classes.TablesManager import TablesManager

def getRealEarnings(tablesManager: TablesManager, profession, logger):
    payouts_list = tablesManager.payouts.scan()["Items"]
    total_earnings = 0
    total_time_delta = 0
    no_stats = 0
    for payout in payouts_list:
        try:
            account = tablesManager.accounts.get_item(Key={"address_": payout["address_"]})["Item"]
        except Exception as e:
            logger.error(f"Error getting account {payout['address_']} from table accounts: {e}")
            raise e
        if "profession" not in account and profession != "mining":
            continue
        elif "profession" in account and account["profession"] != profession:
            continue
            
        if int(payout["time_delta"]) == 0:
            no_stats += 1
            continue
        total_earnings += float(payout["amount_"])
        total_time_delta += int(payout["time_delta"])
    avg_earnings = total_earnings/(len(payouts_list)-no_stats)
    avg_time_delta = total_time_delta/(len(payouts_list)-no_stats)
    avg_daily_earnings = avg_earnings/avg_time_delta*24*60*60
    return avg_daily_earnings
    

