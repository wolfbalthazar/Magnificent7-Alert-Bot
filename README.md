# Ticker Notification System 

A simple Python-based stock market alert system for swing traders. It monitors the 'Magnificent 7' stocks (AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA) on a 4-hour timeframe and sends an email alert when specific technical indicators signal a potential entry point.

## Features
- **Automated Data Fetching**: Retrieves historical data using `yfinance`.
- **Technical Indicators**: Calculates 14-period RSI and 20/50 Simple Moving Averages using the `ta` library.
- **Alert Logic**: 
  - Triggers if RSI falls below 30 (oversold).
  - Triggers if the Fast MA (20) crosses the Slow MA (50) upwards (Golden Cross).
- **Email Notifications**: Sends basic HTML-formatted alerts via SMTP.
- **Database Persistence**: Uses SQLite to remember past alerts and prevent duplicate emails within a 24-hour window.

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Magnificent7-Alert-Bot.git
   cd Magnificent7-Alert-Bot
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your email credentials. (personal info alert!)
   ```env
   SENDER_EMAIL="your_email@gmail.com"
   SENDER_PASSWORD="your_16_character_app_password"
   RECEIVER_EMAIL="receiver_email@example.com"
   ```

## Usage

Start the main monitoring loop:
```bash
python main.py
```
The script will run immediately and is scheduled to re-scan every 4 hours.

To view the history of generated alerts in a clean terminal table, run:
```bash
python show_history.py
```

## Disclaimer
This does not constitute financial advice only educational purposes and my own fun. Always do your own research :)
The code was co-written with antigravity.