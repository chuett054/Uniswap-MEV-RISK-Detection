import pandas as pd
from web3 import Web3
import time

# load csv
df = pd.read_csv("UniswapEvents.csv", low_memory = False)  # <-- replace with your filename

# connect to infura
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/2121bc0855e54a909d6b54a1177c59bd"))

if not w3.is_connected():
    raise Exception("connection failed")

# function to fetch gas price
def fetch_gas_price(tx_hash):
    try:
        tx = w3.eth.get_transaction(tx_hash)
        gas_price_wei = tx['gasPrice']
        gas_price_gwei = w3.from_wei(gas_price_wei, 'gwei')
        return gas_price_gwei
    except Exception as e:
        print(f"error fetching {tx_hash}: {str(e).lower()}")
        return None

# fetch gas prices
gas_prices = []
for tx_hash in df['TX_HASH']:
    gas_price = fetch_gas_price(tx_hash)
    gas_prices.append(gas_price)
    time.sleep(0.05)  # slight pause to be safe

# add to dataframe
df['GAS_PRICE_GWEI'] = gas_prices

# save enriched csv
df.to_csv("uniswap_swaps_enriched.csv", index=False)