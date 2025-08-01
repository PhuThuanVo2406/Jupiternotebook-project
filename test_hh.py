### Q1 ##########################################

import yfinance as yf
import pandas as pd

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()



### Q3 #########################################


import yfinance as yf
import pandas as pd

# Download GME stock data
gme_data = yf.Ticker("GME")
gme_stock = gme_data.history(period="max")

# Reset index and keep necessary columns
gme_stock.reset_index(inplace=True)
gme_stock = gme_stock[["Date", "Open", "High", "Low", "Close", "Volume", "Dividends", "Stock Splits"]]

# Show first few rows
print(gme_stock.head())

### Q4 #############################

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define the URL
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"

# Send a GET request to the URL
try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
except Exception as e:
    print("Error fetching the webpage:", e)
    revenue_gme = pd.DataFrame(columns=["Date", "Revenue"])
else:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all tables
    tables = soup.find_all("table")

    # Search for the GameStop Quarterly Revenue table
    revenue_table = None
    for table in tables:
        if "GameStop Quarterly Revenue" in table.get_text():
            revenue_table = table
            break

    if revenue_table:
        # Read the table into a DataFrame
        revenue_gme = pd.read_html(str(revenue_table))[0]
        revenue_gme.columns = ["Date", "Revenue"]
        revenue_gme.dropna(inplace=True)
        revenue_gme["Revenue"] = revenue_gme["Revenue"].str.replace("$", "").str.replace(",", "")
        print(revenue_gme.head())
    else:
        print("Could not find GameStop Quarterly Revenue table on the page.")
        revenue_gme = pd.DataFrame(columns=["Date", "Revenue"])


### Q2 ##################
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define the URL for Tesla's revenue
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

# Send a GET request to the URL
try:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}")
except Exception as e:
    print("Error fetching the webpage:", e)
    revenue_tesla = pd.DataFrame(columns=["Date", "Revenue"])
else:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all tables
    tables = soup.find_all("table")

    # Search for the Tesla Quarterly Revenue table
    revenue_table = None
    for table in tables:
        if "Tesla Quarterly Revenue" in table.get_text():
            revenue_table = table
            break

    if revenue_table:
        # Convert the HTML table to a DataFrame
        revenue_tesla = pd.read_html(str(revenue_table))[0]
        revenue_tesla.columns = ["Date", "Revenue"]
        revenue_tesla.dropna(inplace=True)

        # Clean dollar signs and commas
        revenue_tesla["Revenue"] = revenue_tesla["Revenue"].str.replace("$", "").str.replace(",", "")
        print(revenue_tesla.head())
    else:
        print("Could not find Tesla Quarterly Revenue table on the page.")
        revenue_tesla = pd.DataFrame(columns=["Date", "Revenue"])
        

        ########.     Q6.     ###################
    import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Load GameStop stock data
gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)

# Manually created GameStop revenue data (You can update this with the latest if needed)
gme_revenue = pd.DataFrame({
    "Date": [
        "2021-01-31", "2020-10-31", "2020-07-31", "2020-04-30", "2020-01-31",
        "2019-10-31", "2019-07-31", "2019-04-30", "2019-01-31"
    ],
    "Revenue": [
        "2224", "1004", "942", "1021", "2194",
        "1439", "1286", "1548", "3086"
    ]
})

# Convert Date to datetime format and sort
gme_revenue["Date"] = pd.to_datetime(gme_revenue["Date"])
gme_revenue = gme_revenue.sort_values("Date")

# Plotting dashboard
fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot GameStop stock price
ax1.plot(gme_data["Date"], gme_data["Close"], label="GME Stock Price", color="red")
ax1.set_xlabel("Date")
ax1.set_ylabel("Stock Price (USD)", color="red")
ax1.tick_params(axis="y", labelcolor="red")

# Create second y-axis for revenue
ax2 = ax1.twinx()
ax2.plot(gme_revenue["Date"], gme_revenue["Revenue"].astype(float), label="Quarterly Revenue", color="blue")
ax2.set_ylabel("Revenue (Million USD)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

# Final touches
plt.title("GameStop Stock Price and Quarterly Revenue")
fig.tight_layout()
plt.grid(True)
plt.show()


#### 5 ########
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# ---------------------------
# Extract Tesla stock data
# ---------------------------
tesla = yf.Ticker("TSLA")
tesla_stock = tesla.history(period="max")
tesla_stock.reset_index(inplace=True)

# ---------------------------
# Extract Tesla revenue data
# ---------------------------
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table")

revenue_table = None
for table in tables:
    if "Tesla Quarterly Revenue" in table.get_text():
        revenue_table = table
        break

if revenue_table:
    tesla_revenue = pd.read_html(str(revenue_table))[0]
    tesla_revenue.columns = ["Date", "Revenue"]
    tesla_revenue.dropna(inplace=True)
    tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace("$", "").str.replace(",", "")
    tesla_revenue["Revenue"] = pd.to_numeric(tesla_revenue["Revenue"], errors='coerce')
    tesla_revenue["Date"] = pd.to_datetime(tesla_revenue["Date"])
else:
    raise Exception("Tesla Revenue table not found")

# ---------------------------
# Plot Dashboard
# ---------------------------
fig, ax1 = plt.subplots(figsize=(14, 6))
plt.suptitle("Tesla Stock Price & Revenue", fontsize=16)

# Plot Tesla Stock
ax1.plot(tesla_stock["Date"], tesla_stock["Close"], label="Stock Price", color="blue")
ax1.set_xlabel("Date")
ax1.set_ylabel("Stock Price (USD)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

# Plot Tesla Revenue
ax2 = ax1.twinx()
ax2.plot(tesla_revenue["Date"], tesla_revenue["Revenue"], label="Revenue", color="green")
ax2.set_ylabel("Revenue (USD Millions)", color="green")
ax2.tick_params(axis="y", labelcolor="green")

# Show plot
plt.show()