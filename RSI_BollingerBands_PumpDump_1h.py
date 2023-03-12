"""
Crypto bot for RSI and Bollinger Bands for timeframe 1h.
RSI<30 and Bollinger band, try Long.
RSI>70 and Bollinger band, try Short.
"""
# Importing libraries:
import pandas as pd
from binance.client import Client
import pytz
import ta
import time
from datetime import datetime, timedelta
import schedule
from plyer import notification
import requests
import credentials

# Crypto pairs are loaded from TXT file:
# Initialize an empty list
crypto_pairs_list = []

# Open the file for reading
with open("crypto_pairs.txt", "r") as file:
    # Loop through the lines of the file
    for line in file:
        # Strip the newline character from the end of the line
        line = line.strip()
        # Add the line to the list of strings
        crypto_pairs_list.append(line)


# Binance credentials:
API_KEY = credentials.api_key
SECRET_KEY = credentials.secret_key
client = Client(API_KEY, SECRET_KEY)

# Discord Bot Token:
BOT_TOKEN = credentials.discord_bot_token

# Show current time at the beginning:
print("Current time is: ", datetime.now().strftime("%H:%M:%S"))


# User inputs:
STARTING_TIME = input("Type starting time in format %H:%M:%S (e.g. 20:00:01): ")
MAX_RUNNING_HOURS = 24
CYCLES = MAX_RUNNING_HOURS - 1
PERCENTAGE_TRIGGER = 4  # For Pump/Dump alert. This could be much bigger (E.g. 10%)


times_for_loop = []  # List for adding times in a Loop
times_for_loop.append(STARTING_TIME)

# Generate time-frame for checking price:
# Convert a string to datetime object:
dt = datetime.strptime(STARTING_TIME, "%H:%M:%S")

for i in range(CYCLES):
    dt = dt + timedelta(minutes=60)
    new_time_dt = datetime.strftime(dt, "%H:%M:%S")
    times_for_loop.append(new_time_dt)

# print(f"List with starting times: {times_for_loop}")
print(f"Script will loop for {MAX_RUNNING_HOURS} hours starting from {STARTING_TIME}.")
print(f"{len(crypto_pairs_list)} crypto pairs will be scanned.")


def GetCandleData(symbol, interval, lookback):
    """Function for Candle information (Open, High, Low, Close, Volume)

    Args:
        symbol (string): Crypto-pair. E.g. ETHUSDT
        interval (integer): Timeframe. E.g.: 5m, 3m, 15m, 4H
        lookback (integer): How many previous candles we need. E.g. 300m.

    Returns:
        _type_: Pandas dataframe with candle information.
    """
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback))
    frame = frame.iloc[:, :6]
    frame.columns = ["Time", "Open", "High", "Low", "Close", "Volume"]
    frame = frame.set_index("Time")
    serbia_timezone = pytz.timezone("Europe/Belgrade")
    frame.index = pd.to_datetime(frame.index, unit="ms")
    # Converting UTC (default for binance lib) to UTC+1
    frame.index = frame.index.tz_localize(pytz.utc).tz_convert(serbia_timezone)
    frame = frame.astype(float)
    return frame


def LoopCryptoPairs():
    """Loop through all Crypto pairs from list crypto_pairs.py"""
    time_now = datetime.now().strftime("%H:%M:%S")
    print("---------------------------------------")
    print(f"Cycle has been started. Time: {time_now}")
    print("---------------------------------------")

    for pair in crypto_pairs_list:
        try:
            # Get candlestick data from 1h timeframe:
            df = GetCandleData(pair, "1h", "60h")

            # Always drop last row in dataframe
            # Reason: Last candlestick isn't closed yet.
            df.drop(df.tail(1).index, inplace=True)

            # Relative Strength Index (RSI):
            # Length is 13, default is 14.
            df["rsi"] = ta.momentum.RSIIndicator(df["Close"], window=13).rsi()

            # Bollinger Bands:
            Bollinger = ta.volatility.BollingerBands(df["Close"], window=30)

            # Channel Indicator Crossing Low Band:
            # If close is lower than bollinger_lband it return 1. Else, it returns 0.
            df["lband"] = Bollinger.bollinger_lband_indicator()

            # Channel Indicator Crossing High Band:
            # If close is higher than bollinger_hband it return 1. Else, it returns 0.
            df["hband"] = Bollinger.bollinger_hband_indicator()

            # Last row of dataframe:
            last_row_df = df.iloc[-1:]

            # Low Bollinger Band from the last row:
            Low_BB = last_row_df["lband"].iloc[-1]

            # High Bollinger Band from the last row:
            High_BB = last_row_df["hband"].iloc[-1]

            # RSI (Relative Strength Index) from the last row:
            rsi = round(last_row_df["rsi"].iloc[-1], 1)

            # We need Close price from penultimate row for percentage change:
            penultimate_row_df = df["Close"].iloc[-2]
            # print(f"Penultimate row is: {penultimate_row_df}")

            # Percentage difference, round on 2 decimals
            percentage_difference = round(
                (
                    (df["Close"].iloc[-1] - penultimate_row_df)
                    / ((penultimate_row_df + df["Close"].iloc[-1]) / 2)
                )
                * 100,
                2,
            )
            # print(f"Percentage difference is: {percentage_difference}")

            # Link for Binance Futures:
            link = "https://www.binance.com/en/futures/" + pair

            # Conditions for Bollinger Bands and RSI Alerts:
            if Low_BB == 1 and rsi <= 30:  # Long signal
                # Discord channel "rsi-bb-long" link:
                url = "https://discord.com/api/v9/channels/1048689731451506789/messages"
                text = f"[{pair}] is bellow Bollinger band. RSI={rsi} at 1h timeframe. Price changed for {percentage_difference}%. Try LONG. Visit: {link}"
                print(text)
                SendDiscordMessage(text, url)
                WindowsNotifications(pair, text)

            elif High_BB == 1 and rsi >= 70:  # Short signal
                # Discord channel "rsi-bb-short" link:
                url = "https://discord.com/api/v9/channels/1048689689219043388/messages"
                text = f"[{pair}] is above Bollinger band. RSI={rsi} at 1h timeframe. Price changed for {percentage_difference}%. Try SHORT. Visit: {link}"
                print(text)
                SendDiscordMessage(text, url)
                WindowsNotifications(pair, text)
            else:
                print(
                    f"[{pair}] passed without triggering Bollinger bands and RSI condition."
                )
                pass

            # Conditions for Pump or Dump Alerts:
            if percentage_difference >= PERCENTAGE_TRIGGER:

                if penultimate_row_df >= df["Close"].iloc[-1]:
                    # Discord channel "drop-alert" link:
                    url = "https://discord.com/api/v9/channels/1050158375037571145/messages"
                    text = f"[{pair}] price has dropped for -{percentage_difference}% at 1h timeframe. Try LONG! Visit: {link}"
                    print(text)
                    SendDiscordMessage(text, url)
                    WindowsNotifications(pair, text)

                elif penultimate_row_df < df["Close"].iloc[-1]:
                    # Discord channel "pump-alert" link:
                    url = "https://discord.com/api/v9/channels/1050158342124863518/messages"
                    text = f"[{pair}] price has pumped for +{percentage_difference}% at 1h timeframe. Try SHORT! Visit: {link}"
                    print(text)
                    SendDiscordMessage(text, url)
                    WindowsNotifications(pair, text)

            else:
                # Price percentage change is lower than defined PERCENTAGE_TRIGGER
                print(f"[{pair}] passed without triggering percentage change in price.")

        except:
            print(
                f"Error, candlestick data for pair [{pair}] wasn't available from Binance Futures."
            )


def SendDiscordMessage(message, channel_url):
    """Function for sending messages to Discord server
    Args:
        message (string): this is message. E.g.: ETHUSDT is above Bollinger band. RSI=75. Try SHORT. Visit LINK
        channel_url (string): Channel URL.
    """
    data = {"content": message}
    header = {"authorization": BOT_TOKEN}

    r = requests.post(channel_url, data=data, headers=header)
    if r.status_code == 200:
        print(f"Discord message sent successfully! Status: {r.status_code}")
    else:
        print(f"Discord message sent failed! Status: {r.status_code}")


def WindowsNotifications(pair, text):
    """Function for Windows notification. Last 5 seconds.
    Args:
        pair (string): pair is crypto-pair from a list (crypto_pairs.py)
        text (string): this is message. E.g.: ETHUSDT is above Bollinger band. RSI=75. Try SHORT. Visit LINK
    """
    notification.notify(
        title=pair,
        message=text,
        # displaying time
        timeout=2,
    )
    # waiting time
    # time.sleep(2)


# Run function in loop. List is times_for_loop = []
for x in times_for_loop:
    schedule.every().day.at(x).do(LoopCryptoPairs)

while True:
    """Function will start in user-defined time. E.g. 20:00:03"""
    schedule.run_pending()
    time.sleep(1)
