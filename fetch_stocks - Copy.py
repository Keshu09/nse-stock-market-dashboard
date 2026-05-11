import requests
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import os

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_file = json_file = [f for f in os.listdir("YOUR_PROJECT_FOLDER_PATH\\")
json_path = f"C:\\Users\\keshu.patidar\\stock_project\\{json_file}"
creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
client = gspread.authorize(creds)
sheet = sheet = client.open_by_key("YOUR_GOOGLE_SHEET_ID_HERE").sheet1

# Alpha Vantage API Key
API_KEY = "YOUR_API_KEY_HERE"

# NSE Stocks — Alpha Vantage uses BSE codes for Indian stocks
stocks = {
    "TCS": "TCS.BSE",
    "Reliance": "RELIANCE.BSE",
    "Infosys": "INFY.BSE",
    "HDFC Bank": "HDFCBANK.BSE"
}

def fetch_stock_data(symbol, name):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize=compact&apikey={API_KEY}"
    response = requests.get(url, verify=False)
    data = response.json()

    if "Time Series (Daily)" not in data:
        print(f"No data for {name}: {data.get('Note') or data.get('Information') or 'Unknown error'}")
        return None

    ts = data["Time Series (Daily)"]
    rows = []
    for date, values in ts.items():
        rows.append({
            "Date": date,
            "Open": float(values["1. open"]),
            "High": float(values["2. high"]),
            "Low": float(values["3. low"]),
            "Close": float(values["4. close"]),
            "Volume": int(values["5. volume"]),
            "Ticker": name
        })
    df = pd.DataFrame(rows)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%m/%d/%Y")
    return df

def fetch_and_update():
    print("Fetching live stock data...")
    all_data = []

    for name, symbol in stocks.items():
        print(f"Fetching {name}...")
        df = fetch_stock_data(symbol, name)
        if df is not None:
            all_data.append(df)
            print(f"Got {len(df)} rows for {name}")
        time.sleep(15)  # Alpha Vantage limit — wait between calls

    if not all_data:
        print("No data fetched!")
        return

    final_df = pd.concat(all_data).reset_index(drop=True)

    existing_data = sheet.get_all_values()
    if not existing_data:
        sheet.update([final_df.columns.tolist()] + final_df.values.tolist())
        print("Written all data!")
    else:
        existing_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])
        existing_keys = set(zip(existing_df["Date"], existing_df["Ticker"]))
        new_rows = final_df[~final_df.apply(lambda row: (row["Date"], row["Ticker"]) in existing_keys, axis=1)]
        if not new_rows.empty:
            sheet.append_rows(new_rows.values.tolist())
            print(f"Added {len(new_rows)} new rows!")
        else:
            print("No new data to add.")

    print(f"Done at {pd.Timestamp.now().strftime('%H:%M:%S')}")

# Run every 15 minutes (Alpha Vantage free tier limit)
while True:
    fetch_and_update()
    print("Waiting 15 minutes...")
    time.sleep(900)