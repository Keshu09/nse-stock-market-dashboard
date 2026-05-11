# NSE Stock Market Live Analytics Dashboard

## 📊 Project Overview
A real-time stock market analytics pipeline that tracks top NSE stocks and visualizes live data on an interactive dashboard.

## 🔧 Tech Stack
- **Python** — Data pipeline
- **Alpha Vantage API** — Live stock data
- **Pandas** — Data processing
- **Google Sheets API** — Cloud data storage
- **Google Looker Studio** — Live dashboard

## 📈 Stocks Tracked
- TCS
- Reliance Industries
- Infosys
- HDFC Bank

## ⚙️ How It Works
1. Python script fetches live stock data from Alpha Vantage API every 15 minutes
2. Data is cleaned and processed using Pandas
3. Automatically written to Google Sheets
4. Looker Studio dashboard reads from Google Sheets and updates in real time

## 📊 Dashboard Features
- KPI Scorecards — Average Close, Max High, Total Volume
- Stock Price Trend — 4 stocks over time
- Volume Distribution — Pie chart by stock
- High vs Low Comparison — Grouped bar chart
- Interactive filters — Date range and Ticker dropdown

## 💡 Key Insights
- HDFC Bank has highest trading volume at 52% of total
- TCS maintains highest price range among all 4 stocks
- All stocks showed correction trend from Feb to May 2026

## 🚀 How to Run
1. Clone this repository
2. Install dependencies: `pip install alpha_vantage requests pandas gspread oauth2client`
3. Add your Alpha Vantage API key and Google Sheets credentials
4. Run: `python fetch_stocks.py`
