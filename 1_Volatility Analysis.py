import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd

st.header("Volatility Analysis")
st.write("This page provides insights into the volatility of the stock market data. The Volatility Analysis Dashboard aims to provide a comprehensive visualization and analysis of the Nifty 50 stocks' volatility over the past year. The dashboard includes key metrics such as the top 10 most volatile stocks, top 10 least volatile stocks, and market summary. The dashboard is designed to help investors make informed decisions based on the volatility of the stocks.")
st.write("The volatility of a stock is a measure of the variation in the stock's price over a period of time. A stock with high volatility is considered riskier, as its price can fluctuate significantly, while a stock with low volatility is considered less risky, as its price is more stable.")
st.write("The dashboard provides insights into the volatility of the Nifty 50 stocks, helping investors identify the most and least volatile stocks in the market.")

st.subheader("Top 10 Most Volatile Stocks")
# Establishing a connection to the MySQL database using SQLAlchemy engine
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")  # root@localhost:3306
try:
    # Connecting to the database engine
    conn = engine.connect()
    
    # Execute SQL query and load data into a Pandas DataFrame
    df = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)
    
except Exception as e:
    st.write("Error: ", e)
finally:
    # Close the connection
    conn.close()
    
# Calculate the volatility of each stock
df = df.sort_values(by=["Ticker", "date"])

df["daily_return"] = df.groupby("Ticker")["close"].pct_change()
volatility = df.groupby("Ticker")["daily_return"].std().reset_index()
  # Annualized volatility
top_10_most_volatile = volatility.sort_values(by="daily_return", ascending=False).head(10).reset_index(drop=True)

fig, ax = plt.subplots()
plt.bar(top_10_most_volatile["Ticker"], top_10_most_volatile["daily_return"], color="skyblue")
plt.xlabel("Stocks")
plt.ylabel("Volatility (Standard Deviation of Daily Returns)")
plt.title("Top 10 Most Volatile Stocks")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
ax.bar_label(ax.containers[0], fontsize=5, padding=3)
st.pyplot(fig)

with st.expander("Volatility Insights"):
    st.write("**1. VEDL is the most volatile stock:** With a standard deviation of daily returns of 0.037, VEDL is the most volatile stock in the Nifty 50.")
    st.write("**2. Significant gap in volatility:** There is a large gap in volatility between VEDL and the next most volatile stock (TATASTEEL with a standard deviation of 0.031).")
    st.write("**3. Majority of stocks have low volatility:** Most of the top 10 most volatile stocks have a standard deviation of daily returns below 0.03.")
    st.write("**4. Range of volatility:** The volatility ranges from a high of 0.037 (VEDL) to a low of 0.025 (HDFCLIFE) within the top 10.")
    st.write("**5. Clustering in lower volatility:** A cluster of stocks (TATAMOTORS, TCS, HINDALCO, JSWSTEEL, UPL, HINDUNILVR) show volatility in a narrower range (around 0.03-0.031).")


st.subheader("Top 10 Least Volatile Stocks")

top_10_least_volatile = volatility.sort_values(by="daily_return", ascending=True).head(10).reset_index(drop=True)

fig, ax = plt.subplots()
plt.bar(top_10_least_volatile["Ticker"], top_10_least_volatile["daily_return"], color="skyblue")
plt.xlabel("Stocks")
plt.ylabel("Volatility (Standard Deviation of Daily Returns)")
plt.title("Top 10 Least Volatile Stocks")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
ax.bar_label(ax.containers[0], fontsize=5, padding=3)
st.pyplot(fig)

with st.expander("Volatilty insights"):
    st.write('**1. SUNPHARMA exhibits the lowest volatility:** SUNPHARMA stock demonstrates the lowest volatility among the top 10 least volatile stocks, with a standard deviation of daily returns at 0.0117328. This indicates it experiences the least price fluctuation compared to the others listed.')
    st.write('**2. HDFCBANK shows the highest volatility:** HDFCBANK stock has the highest volatility among the top 10, with a standard deviation of daily returns at 0.0134898. While it\'s the most volatile in this group, it\'s still considered among the least volatile stocks overall.')
    st.write('**3. Volatility is tightly clustered:** The volatility values for all top 10 stocks are within a narrow range, from approximately 0.0117 to 0.0135. This tight clustering confirms that these are indeed among the least volatile stocks in the market, with relatively small differences in their price fluctuations.')
    st.write('**4. Defensive sectors are prominent:** The list includes stocks from sectors known for stability, such as fast-moving consumer goods (FMCG) like HINDUNILVR, NESTLEIND, and BRITANNIA, and pharmaceuticals like SUNPHARMA and DRREDDY. This sector representation aligns with the characteristic of low volatility.')
    st.write('**5. Financial sector also represented:** ICICIBANK and HDFCBANK from the financial sector are also present in the top 10 least volatile stocks. While the financial sector can sometimes be volatile, these specific banks demonstrate relatively lower volatility compared to the broader market, securing their place in this list.')