import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import pandas as pd
import os

# Streamlit header for the Volatility Analysis dashboard
st.header("Volatility Analysis")

# Brief description of the dashboard
st.write("This page provides insights into the volatility of the stock market data, focusing on the Nifty 50 stocks...")

# Subheader for most volatile stocks
st.subheader("Top 10 Most Volatile Stocks")

# Establishing a connection to the MySQL database using SQLAlchemy engine
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")
try:
    # Connecting to the database
    conn = engine.connect()
    
    # Execute SQL query to fetch data into a Pandas DataFrame
    df = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)
    
    # Sorting data by Ticker and date to ensure proper volatility calculations
    df = df.sort_values(by=["Ticker", "date"])
    
    # Calculating daily returns to measure volatility
    df["daily_return"] = df.groupby("Ticker")["close"].pct_change()
    
    # Computing standard deviation of daily returns as a measure of volatility
    volatility = df.groupby("Ticker")["daily_return"].std().reset_index()
    
    # Define output directory to store volatility analysis results
    output_dir = r"D:\Guvi_Project\DD_Stock_Analysis\Data_Folder\Visualizations"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    
    # Save volatility data to a CSV file
    volatility.to_csv(os.path.join(output_dir, "volatility_analysis.csv"), index=False)
    
    # Reload volatility data from CSV (ensures data integrity)
    volatility = pd.read_csv(os.path.join(output_dir, "volatility_analysis.csv"))
    
    # Store volatility data into the SQL database (replace if already exists)
    volatility.to_sql(name="volatility", con=engine, index=False, if_exists='replace')
 
except Exception as e:
    # Handle exceptions and display error messages in Streamlit
    st.write("Error: ", e)
finally:
    # Ensure database connection is closed properly
    conn.close()

# Identify top 10 most volatile stocks
# Sorting volatility in descending order to get the most volatile stocks
top_10_most_volatile = volatility.sort_values(by="daily_return", ascending=False).head(10).reset_index(drop=True)

# Creating bar chart for most volatile stocks
fig, ax = plt.subplots()
plt.bar(top_10_most_volatile["Ticker"], top_10_most_volatile["daily_return"], color="skyblue")
plt.xlabel("Stocks")
plt.ylabel("Volatility (Standard Deviation of Daily Returns)")
plt.title("Top 10 Most Volatile Stocks")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
ax.bar_label(ax.containers[0], fontsize=5, padding=3)

# Display plot in Streamlit
st.pyplot(fig)

# Insights on most volatile stocks
with st.expander("Volatility Insights"):
    st.write("**1. VEDL is the most volatile stock:** With a standard deviation of daily returns of 0.037, VEDL is the most volatile stock in the Nifty 50.")
    st.write("**2. Significant gap in volatility:** There is a large gap in volatility between VEDL and the next most volatile stock (TATASTEEL with a standard deviation of 0.031).")
    st.write("**3. Majority of stocks have low volatility:** Most of the top 10 most volatile stocks have a standard deviation of daily returns below 0.03.")
    st.write("**4. Range of volatility:** The volatility ranges from a high of 0.037 (VEDL) to a low of 0.025 (HDFCLIFE) within the top 10.")
    st.write("**5. Clustering in lower volatility:** A cluster of stocks (TATAMOTORS, TCS, HINDALCO, JSWSTEEL, UPL, HINDUNILVR) show volatility in a narrower range (around 0.03-0.031).")

# Subheader for least volatile stocks
st.subheader("Top 10 Least Volatile Stocks")

# Identify top 10 least volatile stocks
# Sorting volatility in ascending order to get the least volatile stocks
top_10_least_volatile = volatility.sort_values(by="daily_return", ascending=True).head(10).reset_index(drop=True)

# Creating bar chart for least volatile stocks
fig, ax = plt.subplots()
plt.bar(top_10_least_volatile["Ticker"], top_10_least_volatile["daily_return"], color="skyblue")
plt.xlabel("Stocks")
plt.ylabel("Volatility (Standard Deviation of Daily Returns)")
plt.title("Top 10 Least Volatile Stocks")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
ax.bar_label(ax.containers[0], fontsize=5, padding=3)

# Display plot in Streamlit
st.pyplot(fig)

# Insights on least volatile stocks
with st.expander("Volatility Insights"):
    st.write("**1. SUNPHARMA exhibits the lowest volatility:** SUNPHARMA stock demonstrates the lowest volatility among the top 10 least volatile stocks, with a standard deviation of daily returns at 0.0117328.")
    st.write("**2. HDFCBANK shows the highest volatility:** HDFCBANK stock has the highest volatility among the top 10, with a standard deviation of daily returns at 0.0134898.")
    st.write("**3. Volatility is tightly clustered:** The volatility values for all top 10 stocks are within a narrow range, from approximately 0.0117 to 0.0135.")
    st.write("**4. Defensive sectors are prominent:** The list includes stocks from sectors known for stability, such as FMCG (HINDUNILVR, NESTLEIND, BRITANNIA) and pharmaceuticals (SUNPHARMA, DRREDDY).")
    st.write("**5. Financial sector also represented:** ICICIBANK and HDFCBANK from the financial sector are among the least volatile stocks, showing relative stability compared to the broader market.")
