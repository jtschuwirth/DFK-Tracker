from dfk_commons.classes.APIService import APIService
from dfk_commons.classes.DFKLogger import DFKLogger
from functions.getGardeningEarnings import getGardeningEarnings
from functions.getRealEarnings import getRealEarnings
from functions.getMiningEarnings import getMiningEarnings
from functions.getQuestingUptime import getQuestingUptime, getQuestingUptimeByProfession
from dfk_commons.classes.RPCProvider import RPCProvider
from dfk_commons.classes.TablesManager import TablesManager
from dfk_commons.functions.get_rpc_provider import get_rpc_provider
from dfk_commons.functions.get_tables_manager import get_tables_manager
from dfk_commons.functions.get_api_service import get_api_service
from dfk_commons.functions.get_dfk_logger import get_dfk_logger
from functions.configs import isProd, apiUrl
import logging
import time

logging.basicConfig()
logger = logging.getLogger('stats-tracking')
logger.setLevel(logging.INFO)

def checkGasValues(gas_table, rpcProvider):
    total_gas_cost = 0
    total_gas_price = 0
    gas_list = gas_table.scan()["Items"]
    valid_entries = 0
    for gas_entry in gas_list:
        if "tx_hash" not in gas_entry or gas_entry["tx_hash"] == "":
            continue
        if (int(gas_entry["time_"]) < (int(time.time()) - 7*24*60*60)):
            continue

        try:
            hash = gas_entry["tx_hash"]
            tx = rpcProvider.w3.eth.get_transaction(hash)
            gas_price = tx["gasPrice"]
            gas_cost = tx["gas"]*gas_price
            total_gas_cost += float(gas_cost)
            total_gas_price += float(gas_price)
            valid_entries += 1

            if valid_entries == 200:
                break

        except Exception as e:
            print(e)
    
    if 0<valid_entries:
        avg_gas_cost_results = total_gas_cost/valid_entries
        avg_gas_price_results = (total_gas_price/valid_entries)/10**9
    else:
        avg_gas_cost_results = 0
        avg_gas_price_results = 0

    return avg_gas_cost_results, avg_gas_price_results


def handler(event, context):
    chain = "dfk"
    rpcProvider: RPCProvider = get_rpc_provider(chain, [], logger)
    apiService: APIService = get_api_service(apiUrl, chain)
    tablesManager: TablesManager = get_tables_manager(isProd)
    dfkLogger: DFKLogger = get_dfk_logger(logger)

    quest_per_day = ((24*60)/270)/3
    dfkLogger.info("Starting autoplayer tracking")
    dfkLogger.info("Getting gas values")
    avg_mining_gas_cost_results, avg_mining_gas_price_results = checkGasValues(tablesManager.mining_gas, rpcProvider)
    daily_mining_gas_cost = int(avg_mining_gas_cost_results)*2*quest_per_day*3/10**18
    
    avg_gardening_gas_cost_results, avg_gardening_gas_price_results = checkGasValues(tablesManager.gardening_gas, rpcProvider)
    daily_gardening_gas_cost = int(avg_gardening_gas_cost_results)*2*quest_per_day*3*3/10**18


    dfkLogger.info("Getting uptime values")
    uptime = getQuestingUptime(tablesManager)
    uptime_mining = getQuestingUptimeByProfession(tablesManager, "mining")
    uptime_gardening = getQuestingUptimeByProfession(tablesManager, "gardening")

    dfkLogger.info("Getting earnings")
    mining_earnings = int(getMiningEarnings(quest_per_day, apiService, rpcProvider, logger))/10**18
    gardening_earnings = int(getGardeningEarnings(quest_per_day, apiService, rpcProvider, logger))/10**18

    mining_real_earnings = getRealEarnings(tablesManager, "mining")
    gardening_real_earnings = getRealEarnings(tablesManager, "gardening")

    dfkLogger.info("Calculating profits")
    expected_avg_mining_profit = mining_earnings - daily_mining_gas_cost
    expected_avg_gardening_profit = gardening_earnings - daily_gardening_gas_cost

    dfkLogger.info("Saving data")
    item = {
        "time_": str(int(time.time())),
        "uptime": str(uptime),
        "uptime_mining": str(uptime_mining),
        "uptime_gardening": str(uptime_gardening),

        "daily_avg_mining_earnings": str(mining_earnings),
        "daily_avg_gardening_earnings": str(gardening_earnings),

        "daily_real_avg_mining_profit": str(mining_real_earnings),
        "daily_real_avg_gardening_profit": str(gardening_real_earnings),

        "daily_expected_avg_mining_profit": str(expected_avg_mining_profit),
        "daily_expected_avg_gardening_profit": str(expected_avg_gardening_profit),

        "daily_avg_mining_gas_cost": str(daily_mining_gas_cost),
        "daily_avg_gardening_gas_cost": str(daily_gardening_gas_cost),

        "avg_mining_gas_price": str(avg_mining_gas_price_results),
        "avg_gardening_gas_price": str(avg_gardening_gas_price_results)
    }

    dfkLogger.info(item)
    tablesManager.autoplayer_tracking.put_item(Item=item)

    return item