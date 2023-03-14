import requests
import credentials

# Discord Bot Token:
BOT_TOKEN = credentials.discord_bot_token
# Discord bot token look like this: MTA0O...,
# but you must add string 'Bot 'at the begining, like this: "Bot MTA0O..."


def SendDiscordMessage(message, channel_url):
    """Function for sending messages to Discord server
    Args:
        message (string): this is message. E.g.: [ETHUSDT] is above Bollinger band. RSI=75. Try SHORT. Visit LINK
        channel_url (string): Channel URL.
    """
    data = {"content": message}
    header = {"authorization": BOT_TOKEN}

    r = requests.post(channel_url, data=data, headers=header)
    if r.status_code == 200:
        print(f"Discord message sent successfully! Status: {r.status_code}")
    else:
        print(f"Discord message sent failed! Status: {r.status_code}")


if __name__ == "__main__":
    SendDiscordMessage(
        "Test message",
        "https://discord.com/api/v9/channels/1050158342124863518/messages",
    )
