from dfk_commons.classes.APIService import APIService
from dfk_commons.classes.DFKLogger import DFKLogger
from functions.getGardeningEarnings import getGardeningEarnings
from functions.getRealEarnings import getRealEarnings
from functions.getMiningEarnings import getMiningEarnings
from functions.checkGasValues import checkGasValues
from functions.getQuestingUptime import getQuestingUptimeByProfession
from dfk_commons.classes.RPCProvider import RPCProvider
from dfk_commons.classes.TablesManager import TablesManager
from dfk_commons.functions.get_rpc_provider import get_rpc_provider
from dfk_commons.functions.get_tables_manager import get_tables_manager
from dfk_commons.functions.get_api_service import get_api_service
from dfk_commons.functions.get_dfk_logger import get_dfk_logger
from functions.configs import isProd, apiUrl, apiKey
import logging
import time

logging.basicConfig()
logger = logging.getLogger('stats-tracking')
logger.setLevel(logging.INFO)

def handler(event, context):
    chain = event["chain"]
    profession= event["profession"]
    rpcProvider: RPCProvider = get_rpc_provider(chain, logger)
    apiService: APIService = get_api_service(apiUrl, apiKey,  chain)
    tablesManager: TablesManager = get_tables_manager(isProd)
    dfkLogger: DFKLogger = get_dfk_logger(logger)

    if profession == "mining":
        gas_table = tablesManager.mining_gas
        stats_table = tablesManager.mining_stats
        quest_per_day = ((24*60)/270)/3
    elif profession == "gardening":
        gas_table = tablesManager.gardening_gas
        stats_table = tablesManager.gardening_stats
        quest_per_day = ((24*60)/270)/3
    elif profession == "fishing":
        gas_table = tablesManager.fishing_gas
        stats_table = tablesManager.fishing_stats
        quest_per_day = ((24*60)/180)/3
    elif profession == "foraging":
        gas_table = tablesManager.foraging_gas
        stats_table = tablesManager.foraging_stats
        quest_per_day = ((24*60)/180)/3

    dfkLogger.info(f"Starting autoplayer tracking for {profession}")
    dfkLogger.info("Getting gas values")

    if isProd:
        avg_cost_results, avg_gas_price_results = checkGasValues(gas_table, rpcProvider)
        daily_gas_cost = int(avg_cost_results)*2*quest_per_day*3/10**18
        
    else:
        daily_gas_cost=0
        avg_cost_results=0
        avg_gas_price_results=0

    dfkLogger.info("Getting uptime values")
    uptime = getQuestingUptimeByProfession(tablesManager, profession)

    dfkLogger.info("Getting expected earnings")
    if profession == "mining":
        earnings = int(getMiningEarnings(quest_per_day, apiService, rpcProvider, logger))/10**18
    elif profession == "gardening":
        earnings = int(getGardeningEarnings(quest_per_day, apiService, rpcProvider, logger))/10**18
    elif profession == "fishing":
        earnings = 0
    elif profession == "foraging":
        earnings = 0

    dfkLogger.info("Getting real earnings")
    real_earnings = getRealEarnings(tablesManager, profession)

    dfkLogger.info("Calculating profits")
    expected_avg_profit = earnings - daily_gas_cost

    dfkLogger.info("Saving data")
    item = {
        "time_": str(int(time.time())),
        "uptime": str(uptime),
        "daily_expected_avg_earnings": str(earnings),
        "daily_real_avg_profit": str(real_earnings),
        "daily_expected_avg_profit": str(expected_avg_profit),
        "daily_avg_gas_cost": str(daily_gas_cost),
        "avg_gas_price": str(avg_gas_price_results),
    }

    dfkLogger.info(item)
    if isProd:
        stats_table.put_item(Item=item)

    return item