

```markdown
# Crypto Price Bot

Telegram bot for real-time monitoring of TON, USDT, and FREENET cryptocurrency rates.

## Description

The bot automatically sends current cryptocurrency rates to a specified chat or channel at a set interval. It displays prices in USD and RUB, as well as percentage changes.

## Features

- Monitoring of TON/USDT, USDT/RUB, and FREENET/USDT rates
- Conversion to rubles
- Tracking of percentage rate changes
- Customizable update interval
- Custom signature with link support

## Installation and Setup

### Prerequisites

- Python 3.7+
- Telegram bot (created via @BotFather)
- Telegram chat or channel ID

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crypto-price-bot.git
cd crypto-price-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create an `.env` file in the project root directory and fill it with the following data:
```
TELEGRAM_BOT_TOKEN=your_bot_token
CHAT_ID=chat_identifier
CUSTOM_SIGNATURE=[BINGX](https://bingx.com/partner/TONFREENET/) | [TonTradingBot](https://t.me/tontrade?start=XsDjLHUq)
UPDATE_INTERVAL=5
```

### .env Parameters Description

| Parameter | Description | Example |
|----------|----------|--------|
| TELEGRAM_BOT_TOKEN | Your Telegram bot token obtained from @BotFather | `5432112345:AAHxyz123456789abcdefghijklmnopqrstuv` |
| CHAT_ID | ID of the chat or channel where the bot will send messages | `-1001234567890` |
| CUSTOM_SIGNATURE | Custom signature with Markdown formatting support | `[BINGX](https://bingx.com/partner/TONFREENET/) \| [TonTradingBot](https://t.me/tontrade?start=XsDjLHUq)` |
| UPDATE_INTERVAL | Rate update interval in minutes | `5` |

### Running

```bash
python bot.py
```

## Server Deployment

### Using systemd (Linux)

1. Create a service file:
```bash
sudo nano /etc/systemd/system/crypto-bot.service
```

2. Add the following content:
```
[Unit]
Description=Telegram Crypto Bot
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/bot/folder
ExecStart=/path/to/python3 /path/to/bot/folder/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Activate and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable crypto-bot.service
sudo systemctl start crypto-bot.service
```

### Using screen (alternative method)

```bash
screen -S crypto-bot
python bot.py
# Press Ctrl+A, then D to detach from the session
```

## How to Get Chat ID

1. Add the bot to the desired chat or channel
2. Send a message to this chat
3. Open in browser: `https://api.telegram.org/bot<your_token>/getUpdates`
4. Find `"chat":{"id":XXXXXXXXX}` in the response - this is the chat ID

## Notes

- For channels, the bot must be added as an administrator
- For correct display of percentage changes, at least two updates are required
- APIs for getting rates have request limits, consider this when setting the update interval

## License

MIT

## Authors

ITDev && incteam
```
