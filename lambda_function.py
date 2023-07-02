from functions.initTables import initTrackingTable, initGasTable
from functions.getMiningEarnings import getMiningEarnings
import time

def handler(event, context):
    quest_per_day = 1.84615
    tracking_table = initTrackingTable()
    gas_table = initGasTable()
    gas_list = gas_table.scan()["Items"]
    total_gas_cost = 0
    for gas_entry in gas_list:
        total_gas_cost += float(gas_entry["gas_cost"])
        gas_table.delete_item(Key={"time_": gas_entry["time_"]})
    if len(gas_list) == 0:
        avg_gas_cost = 0
    else:
        avg_gas_cost = total_gas_cost/len(gas_list)

    mining_earnings = getMiningEarnings(quest_per_day)
    tracking_table.put_item(Item={
            "time_": str(int(time.time())),
            "daily_avg_earnings": str(int(mining_earnings)/10**18),
            "daily_avg_gas_cost": str(avg_gas_cost*quest_per_day),
        })
    return {
        "time_": str(int(time.time())),
        "daily_avg_earnings": str(int(mining_earnings)/10**18),
        "daily_avg_gas_cost": str(avg_gas_cost*quest_per_day),
    }