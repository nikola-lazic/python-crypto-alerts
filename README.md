# **Crypto bot Alerts**

![Python logo](/img/binance-logo.jpeg) ![Python logo](/img/python-logo.png) ![Discord logo](/img/discord-logo-blue.png)

</br>This Python script scans the Crypto pairs which are loaded from TXT file. prices and examines whether the Bollinger bands and RSI have been triggered in a 1-hour timeframe.
</br>Besides this two technical conditions, we are also tracking percentage of price changing (Pump and Dump).
- Timeframe: 1h
- Technical indicators: Bollinger Bands and RSI (Relative Strength Index)
- Candlestick data (Open, High, Low, Close, Volume) are from Binance Spot, but given link at the end of process is for Binance Futures. 
- Beware that there is a slight difference in price between Spot and Futures

Using this script isn't financial advice in any case, it is for educational purposes!

---

## **Table of Contents**
- [What will you learn?](#what-will-you-learn?)
- [Requirements](#requirements)
- [How to use?](#how-to-use)
- [How APIs are set?](#how-apis-are-set)
- [Useful snippets](#useful-snippets)

---

### **What will you learn?**
- How to use unofficial binance.client library and get Candlestick data
- Use ta library for checking Bollinger Bands and RSI (Relative Strength Index) 
- How to send an message into Discord channel
- How to pop-up Windows Notifications

---

### **Requirements**
- Please, check necessary libraries: 
```
pip install -r requirements.txt
```
- Binance API and Secret key (it's free)
- Discord bot token (it's free)

---

### **How to use?**
Run Python script RSI_BollingerBands_PumpDump_1h.py.
</br>In terminal, we will see print message with current time and user input for starting time. Considering that script is written for 1H timeframe, I always insert 00 minutes and 01 secund, example: 21:00:01, 22:00:01, ..., 00:00:01.

</br>Terminal:
```
Current time is:  20:40:54
Type starting time in format %H:%M:%S (e.g. 20:00:01): 21:00:01
```
After this, we will see this message:
```
Script will loop for 24 hours starting from 21:00:01.
81 crypto pairs will be scanned.
```
Crypto pairs are written in crypto_pairs.txt. Some of them are:
```
ETHUSDT
BTCUSDT
DOGEUSDT
APTUSDT
MASKUSDT
XRPUSDT
MATICUSDT
```
At this moment, we are waiting the script to start, and when it happens, we will get messages into terminal. For the example:
```
---------------------------------------
Cycle has been started. Time: 21:00:01
---------------------------------------
[ETHUSDT] passed without triggering Bollinger bands and RSI condition.
[ETHUSDT] passed without triggering percentage change in price.
[BTCUSDT] passed without triggering Bollinger bands and RSI condition.
[BTCUSDT] passed without triggering percentage change in price.
[DOGEUSDT] passed without triggering Bollinger bands and RSI condition.
[DOGEUSDT] passed without triggering percentage change in price.
[APTUSDT] passed without triggering Bollinger bands and RSI condition.
.
.
.
.
.
[INJUSDT] passed without triggering Bollinger bands and RSI condition.
[INJUSDT] price has pumped for +6.41% at 1h timeframe. Try SHORT! Visit: https://www.binance.com/en/futures/INJUSDT
Discord message sent successfully! Status: 200
.
.
.
```
As we can see from the log above, [INJUSDT] price has pumped for +6.41% at 1h timeframe.

</br> Windows notification look like this:
</br>![win-notification](/img/win-notification.JPG)
</br>Discord message look like this:
</br>![discord-notification](/img/discord-notification.JPG)

Considering that we are in Bear market, I set:
```
PERCENTAGE_TRIGGER = 4
```
Have in mind that this value could (and should) be bigger in Bull market, e.g. 10.
</br>From this moment, script will loop for next 24 hours.

---

### **How APIs are set?**
For this script Binance API and their Secret code is must. Good thing, it's free.
</br> You can avoid using Discord API if you don't need sending messages into Discord channel via Python. It was for my learning purposes and also it's nice thing to receive an notification on smartphone.
</br> All credentials are stored into credentials.py. It look's like this:
</br>![credentials](/img/creds.png)
NOTE: Discord token have string "Bot " before token. Otherwise, it won't work.

---

### **Useful snippets**
I added 3 useful snippets, which are also used in this project:
- Discord_message.py for sending a message into Discord channel.
- Get_all_crypto_pairs.py for getting all USDT crypto pairs from Binance, without BUSD pairs.
- Percentage_change_of_price.py for checking the percentage change of price. Data are stored in dictionary.
