# Script for getting all USDT Crypto pairs from Binance.com, without BUSD pairs:

import os, sys
from binance.client import Client

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import credentials

# Binance credentials:
apiKey = credentials.api_key
secretKey = credentials.secret_key
client = Client(apiKey, secretKey)

# Empty list for crypto pairs:
crypto_pairs = []

all_binance_pairs = client.get_all_tickers()

for crypto_pair in all_binance_pairs:
    # Find USDT pairs, but NO BUSD pairs:
    if crypto_pair["symbol"].find("USDT") != -1 and crypto_pair["symbol"][:3] != "BUSD":
        # crypto_pairs.append(crypto_pair["symbol"])
        crypto_pairs.append(crypto_pair)
        # print(ticker["symbol"])
        print(crypto_pair)
        # print(type(crypto_pair))

print(f"Number of Crypto pairs: {(len(crypto_pairs))}.")

"""
# open file in write mode
with open(r"crypto_pairs.txt", "w") as fp:
    for pair in crypto_pairs:
        # write each item on a new line
        fp.write("%s\n" % pair)
    print("Done")
"""
