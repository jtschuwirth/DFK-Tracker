from functions.classes.APIService import APIService
from functions.getGardeningEarnings import getGardeningEarnings
from functions.getRealEarnings import getRealEarnings
from functions.getMiningEarnings import getMiningEarnings
from functions.getQuestingUptime import getQuestingUptime
from functions.classes.RPCProvider import RPCProvider, get_rpc_provider
from functions.classes.TablesManager import TablesManager
from functions.classes.Config import isProd
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    chain = "dfk"
    rpcProvider: RPCProvider = get_rpc_provider(chain, [], logger)
    apiService = APIService(chain)
    tablesManager = TablesManager(isProd)

    quest_per_day = 1.84615
    avg_gas_cost_results = []
    avg_gas_price_results = []

    for gas_table in [tablesManager.mining_gas, tablesManager.gardening_gas]:
        total_gas_cost = 0
        total_gas_price = 0
        gas_list = gas_table.scan()["Items"]
        entries = len(gas_list)
        for gas_entry in gas_list:
            hash = gas_entry["tx_hash"]
            try:
                tx = rpcProvider.w3.eth.get_transaction(hash)
                gas_price = tx["gasPrice"]
                gas_cost = tx["gas"]*gas_price
                total_gas_cost += float(gas_cost)
                total_gas_price += float(gas_price)

            except Exception as e:
                print(e)

        if len(gas_list) == 0:
            avg_gas_cost_results.append(0)
            avg_gas_price_results.append(0)
        elif 0<entries:
            avg_gas_cost_results.append(total_gas_cost/entries)
            avg_gas_price_results.append((total_gas_price/entries)/10**9)
        else:
            avg_gas_cost_results.append(0)
            avg_gas_price_results.append(0)
        
    uptime = getQuestingUptime(tablesManager)

    mining_earnings = int(getMiningEarnings(quest_per_day, apiService, rpcProvider))/10**18
    gardening_earnings = int(getGardeningEarnings(quest_per_day, apiService, rpcProvider))/10**18

    mining_real_earnings = getRealEarnings(tablesManager, "mining", logger)
    gardening_real_earnings = getRealEarnings(tablesManager, "gardening", logger)

    daily_mining_gas_cost = int(avg_gas_cost_results[0])*2*quest_per_day*3/10**18
    daily_gardening_gas_cost = int(avg_gas_cost_results[1])*2*quest_per_day*3/10**18

    expected_avg_mining_profit = mining_earnings - daily_mining_gas_cost
    expected_avg_gardening_profit = gardening_earnings - daily_gardening_gas_cost

    item = {
        "time_": str(int(time.time())),
        "uptime": str(uptime),

        "daily_avg_mining_earnings": str(mining_earnings),
        "daily_avg_gardening_earnings": str(gardening_earnings),

        "daily_real_avg_mining_profit": str(mining_real_earnings),
        "daily_real_avg_gardening_profit": str(gardening_real_earnings),

        "daily_expected_avg_mining_profit": str(expected_avg_mining_profit),
        "daily_expected_avg_gardening_profit": str(expected_avg_gardening_profit),

        "daily_avg_mining_gas_cost": str(daily_mining_gas_cost),
        "daily_avg_gardening_gas_cost": str(daily_gardening_gas_cost),

        "avg_mining_gas_price": str(avg_gas_price_results[0]),
        "avg_gardening_gas_price": str(avg_gas_price_results[1])
    }

    tablesManager.autoplayer_tracking.put_item(Item=item)

    return item