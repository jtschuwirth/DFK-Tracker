from functions.getRealEarnings import getRealEarnings
from functions.initTables import initTrackingTable, initGasTable, init_settings_table, init_account_table
from functions.getMiningEarnings import getMiningEarnings
from functions.getQuestingUptime import getQuestingUptime
from functions.provider import get_provider
import time

w3 = get_provider("dfk")

def handler(event, context):
    quest_per_day = 1.84615
    tracking_table = initTrackingTable()
    gas_table = initGasTable()
    settings_table = init_settings_table()
    accounts_table = init_account_table()
    gas_list = gas_table.scan()["Items"]
    total_gas_cost = 0
    total_gas_price = 0
    c = 0
    for gas_entry in gas_list:
        hash = gas_entry["tx_hash"]
        try:
            if c < 50:   
                tx = w3.eth.getTransaction(hash)
                gas_price = tx["gasPrice"]
                gas_cost = tx["gas"]*gas_price
                total_gas_cost += float(gas_cost)
                total_gas_price += float(gas_price)
                c+=1
        except Exception as e:
            print(e)
        #gas_table.delete_item(Key={"time_": gas_entry["time_"]})

    if len(gas_list) == 0:
        avg_gas_cost = 0
        avg_gas_price = 0
    elif 0<c:
        avg_gas_cost = total_gas_cost/c
        avg_gas_price = (total_gas_price/c)/10**9
    else:
        avg_gas_cost = 0
        avg_gas_price = 0
        
    uptime = getQuestingUptime(accounts_table)

    mining_earnings = int(getMiningEarnings(quest_per_day))/10**18
    real_earnings = getRealEarnings()
    daily_gas_cost = int(avg_gas_cost)*2*quest_per_day*3/10**18
    expected_avg_profit = mining_earnings - daily_gas_cost
    item = {
        "time_": str(int(time.time())),
        "daily_avg_earnings": str(mining_earnings),
        "daily_real_avg_profit": str(real_earnings),
        "daily_expected_avg_profit": str(expected_avg_profit),
        "daily_avg_gas_cost": str(daily_gas_cost),
        "avg_gas_price": str(avg_gas_price),
        "uptime": str(uptime),
    }
    tracking_table.put_item(Item=item)
    if expected_avg_profit < 0 or real_earnings < 0:
        settings_table.update_item(
            Key={"key_":"mining"},
            UpdateExpression="set enabled=:enabled",
            ExpressionAttributeValues={
                ":enabled": False
            }
        )
        settings_table.update_item(
            Key={"key_":"buyer_settings"},
            UpdateExpression="set enabled=:enabled",
            ExpressionAttributeValues={
                ":enabled": False
            }
        )
        
    return item