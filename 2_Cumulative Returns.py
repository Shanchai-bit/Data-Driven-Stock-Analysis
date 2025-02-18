import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Streamlit Header
st.header("Cumulative Return over Time")

# Description of the dashboard functionality
st.write('**Cumulative Return for Top 5 Performing Stocks:** A line chart displaying cumulative returns for each stock over the year (an increasing trend indicates positive performance).')

# Establishing a connection to the MySQL database using SQLAlchemy
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")

try:
    # Connecting to the database
    conn = engine.connect()
    
    # Fetching stock data from the database
    df = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)
    
    # Sorting data by Ticker and Date for correct cumulative return calculation
    df = df.sort_values(by=["Ticker", "date"])

    # Calculating daily returns as percentage change
    df["Daily Return"] = df.groupby("Ticker")["close"].pct_change()

    # Calculating cumulative return using cumulative product formula
    df["Cumulative Return"] = df.groupby("Ticker")["Daily Return"].transform(lambda x: (1 + x).cumprod())

    # Identify the latest available date in the dataset
    latest_date = df["date"].max()

    # Selecting the top 5 performing stocks based on their cumulative return on the latest date
    top_5_stocks = df[df["date"] == latest_date].nlargest(5, "Cumulative Return")["Ticker"].tolist()

    # Filtering dataset to retain only data for the top 5 stocks
    df_top = df[df["Ticker"].isin(top_5_stocks)]
    
    # Define local storage path
    output_dir = r"D:\Guvi_Project\DD_Stock_Analysis\Data_Folder\Visualizations"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    
    # Save filtered data to CSV
    Cumulative_return = df_top.to_csv(os.path.join(output_dir, "Cumulative_return.csv"), index=False)
    
    # Store the data in SQL (replacing if table exists)
    #Cumulative_return.to_sql(name="Cumulative_return", con=engine, index=False, if_exists='replace')
 
except Exception as e:
    # Handling errors and displaying messages in Streamlit
    st.write("Error: ", e)

finally:
    # Ensure database connection is closed properly
    conn.close()
    

# Creating a visualization
fig, ax = plt.subplots(figsize=(12, 6))

# Plot cumulative return for each of the top 5 stocks
for stock in top_5_stocks:
    stock_data = df_top[df_top["Ticker"] == stock]
    ax.plot(stock_data["date"], stock_data["Cumulative Return"], label=stock)

# Setting labels and title
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Return")
ax.set_title("Cumulative Return Over Time (Top 5 Stocks)")
ax.legend()
ax.grid()

# Display plot in Streamlit
st.pyplot(fig)

# Expander for insights
with st.expander("Cumulative Returns Insights"):
    st.write("**1. TRENT Outperforms Significantly:** TRENT exhibits the highest cumulative return over the entire period. Its trajectory is consistently upward and steeper than the other stocks, indicating strong and sustained growth.")
    st.write("**2. BEL Shows Robust Growth, Though with Volatility:** BEL demonstrates a strong upward trend, but with more fluctuations compared to TRENT. This suggests higher volatility, meaning its price experienced more significant swings but still resulted in strong overall growth.")
    st.write("**3. M&M and BAJAJ-AUTO Show Moderate Growth:** Both M&M and BAJAJ-AUTO exhibit positive cumulative returns, but their growth is notably less pronounced compared to TRENT and BEL. Their lines show a more gradual and moderate increase, indicating steady but less aggressive growth.")
    st.write("**4. BHARTIARTL Lags Behind:** BHARTIARTL shows the least impressive cumulative return among the five. Its growth is slow and relatively stagnant compared to the others, indicating significantly lower returns and possible challenges in its performance.")
    st.write("**5. Divergence in Performance Over Time:** Initially, the stocks were relatively close in terms of cumulative return. However, as time passes, TRENT and BEL pull far ahead, while M&M, BAJAJ-AUTO, and particularly BHARTIARTL lag increasingly behind. This highlights the importance of long-term investment horizons for capturing significant growth differences.")
