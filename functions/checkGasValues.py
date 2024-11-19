import time

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