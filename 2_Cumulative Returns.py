import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.header("Cumulative Return over time")
st.write('**Cumulative Return for Top 5 Performing Stocks:** A line chart displaying cumulative returns for each stock over the year (increasing trend indicates positive performance).')
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
    

# Sort values by date for proper cumulative return calculation
df = df.sort_values(by=["Ticker", "date"])

# Calculate daily returns for each stock
df["Daily Return"] = df.groupby("Ticker")["close"].pct_change()

# Calculate cumulative return as a running product of (1 + daily return)
df["Cumulative Return"] = df.groupby("Ticker")["Daily Return"].transform(lambda x: (1 + x).cumprod())

# Identify the latest date in the dataset
latest_date = df["date"].max()

# Get the top 5 performing stocks based on cumulative return at year-end
top_5_stocks = df[df["date"] == latest_date].nlargest(5, "Cumulative Return")["Ticker"]

# Filter dataset for only the top 5 stocks
df_top = df[df["Ticker"].isin(top_5_stocks)]

# Create a figure
fig, ax = plt.subplots(figsize=(12, 6))

# Plot cumulative return for top 5 stocks
for stock in top_5_stocks:
    stock_data = df_top[df_top["Ticker"] == stock]
    ax.plot(stock_data["date"], stock_data["Cumulative Return"], label=stock)

# Set labels and title
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
ax.set_title("Cumulative Return Over Time (Top 5 Stocks)")
ax.legend()
ax.grid()

# Display plot in Streamlit
st.pyplot(fig)

with st.expander("Cumulative returns insights"):
    st.write("**1. TRENT Outperforms Significantly: ** The chart clearly shows that TRENT exhibits the highest cumulative return over the entire period.  Its trajectory is consistently upward and steeper than the other stocks, indicating a strong and sustained growth. This suggests that TRENT has been the most successful investment among the top 5 stocks during this timeframe.")
    st.write("**2. BEL Shows Robust Growth, Though with Volatility:**  BEL also demonstrates a strong upward trend, signifying substantial growth. However, its path is marked by more fluctuations (ups and downs) compared to TRENT. This suggests higher volatility for BEL, meaning its price experienced more significant swings during the period, but still resulted in strong overall growth.")
    st.write("**3. M&M and BAJAJ-AUTO Show Moderate Growth:**  Both M&M and BAJAJ-AUTO exhibit positive cumulative returns, but their growth is notably less pronounced compared to TRENT and BEL. Their lines show a more gradual and moderate increase, indicating steady but less explosive growth")
    st.write("**4. BHARTIARTL Lags Behind:**  BHARTIARTL shows the least impressive cumulative return among the five. Its growth is slow and relatively stagnant compared to the others. This suggests that BHARTIARTL experienced significantly lower returns and potentially faced challenges or slower growth drivers during the observed period.")
    st.write("**5. Divergence in Performance Over Time:**  As time progresses, the performance gap between the stocks widens significantly.  Initially, the stocks were relatively close in terms of cumulative return. However, as time passes, TRENT and BEL pull far ahead, while M&M, BAJAJ-AUTO, and particularly BHARTIARTL lag increasingly behind. This highlights the importance of long-term investment horizons for capturing significant growth differences and the potential for substantial variation in individual stock performance, even among top companies.")