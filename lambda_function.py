from dfk_commons.classes.APIService import APIService
from functions.getGardeningEarnings import getGardeningEarnings
from functions.getRealEarnings import getRealEarnings
from functions.getMiningEarnings import getMiningEarnings
from functions.getQuestingUptime import getQuestingUptime, getQuestingUptimeByProfession
from dfk_commons.classes.RPCProvider import RPCProvider
from dfk_commons.classes.TablesManager import TablesManager
from dfk_commons.functions.get_rpc_provider import get_rpc_provider
from dfk_commons.functions.get_tables_manager import get_tables_manager
from dfk_commons.functions.get_api_service import get_api_service
from functions.configs import isProd
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def checkGasValues(gas_table, rpcProvider):
    avg_gas_cost_results = []
    avg_gas_price_results = []
    total_gas_cost = 0
    total_gas_price = 0
    gas_list = gas_table.scan()["Items"]
    entries = len(gas_list)
    not_valids = 0
    for gas_entry in gas_list:
        if "tx_hash" not in gas_entry or gas_entry["tx_hash"] == "":
            not_valids += 1
            continue
        if (int(gas_entry["time_"]) < (int(time.time()) - 7*24*60*60)):
            not_valids += 1
            continue
        try:
            tx = rpcProvider.w3.eth.get_transaction(hash)
            gas_price = tx["gasPrice"]
            gas_cost = tx["gas"]*gas_price
            total_gas_cost += float(gas_cost)
            total_gas_price += float(gas_price)

        except Exception as e:
            not_valids += 1
            print(e)

    if 0<entries:
        avg_gas_cost_results.append(total_gas_cost/(entries-not_valids))
        avg_gas_price_results.append((total_gas_price/(entries-not_valids))/10**9)
    else:
        avg_gas_cost_results.append(0)
        avg_gas_price_results.append(0)

    return avg_gas_cost_results, avg_gas_price_results


def handler(event, context):
    chain = "dfk"
    rpcProvider: RPCProvider = get_rpc_provider(chain, [], logger)
    apiService: APIService = get_api_service(chain)
    tablesManager: TablesManager = get_tables_manager(isProd)

    quest_per_day = 1.84615
    for gas_table in [tablesManager.mining_gas, tablesManager.gardening_gas]:
        avg_gas_cost_results, avg_gas_price_results = checkGasValues(gas_table, rpcProvider)

    uptime = getQuestingUptime(tablesManager)
    uptime_mining = getQuestingUptimeByProfession(tablesManager, "mining")
    uptime_gardening = getQuestingUptimeByProfession(tablesManager, "gardening")

    mining_earnings = int(getMiningEarnings(quest_per_day, apiService, rpcProvider, logger))/10**18
    gardening_earnings = int(getGardeningEarnings(quest_per_day, apiService, rpcProvider, logger))/10**18

    mining_real_earnings = getRealEarnings(tablesManager, "mining")
    gardening_real_earnings = getRealEarnings(tablesManager, "gardening")

    daily_mining_gas_cost = int(avg_gas_cost_results[0])*2*quest_per_day*3/10**18
    daily_gardening_gas_cost = int(avg_gas_cost_results[1])*2*quest_per_day*3*3/10**18

    expected_avg_mining_profit = mining_earnings - daily_mining_gas_cost
    expected_avg_gardening_profit = gardening_earnings - daily_gardening_gas_cost

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

        "avg_mining_gas_price": str(avg_gas_price_results[0]),
        "avg_gardening_gas_price": str(avg_gas_price_results[1])
    }

    tablesManager.autoplayer_tracking.put_item(Item=item)

    return item