import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Establishing a connection to the MySQL database using SQLAlchemy engine
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")  # root@localhost:3306
try:
    # Connecting to the database engine
    conn = engine.connect()
    
    # Execute SQL query and load data into a Pandas DataFrame
    all_data_df = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)
    
    #Python DataFrame for Key Metrics:
    #Top 10 Green Stocks: Sort the stocks based on their yearly return and select the top 10.

    # Convert 'date' to datetime for sorting
    all_data_df["date"] = pd.to_datetime(all_data_df["date"])

    # Sort data for return calculations
    df_stock = all_data_df.sort_values(by=["Ticker", "date"])

    # Get first and last closing prices for each stock
    first_prices = df_stock.groupby("Ticker")["close"].first()
    last_prices = df_stock.groupby("Ticker")["close"].last()

    # Compute yearly return
    stock_returns = pd.DataFrame({
        "Ticker": first_prices.index,  
        "yearly_return": (last_prices / first_prices) - 1  # Apply return formula
    }).reset_index(drop=True)


    #main dataframe stock_returns
    
    st.header("Stock Analysis Dashboard")
    st.write("This dashboard provides insights into the stock market data. The Stock Performance Dashboard aims to provide a comprehensive visualization and analysis of the Nifty 50 stocks' performance over the past year. The dashboard includes key metrics such as the top 10 green stocks, top 10 loss stocks, and market summary. The dashboard is designed to help investors make informed decisions based on the performance of the stocks.")
    
    top_10_green_stocks = stock_returns.sort_values(by="yearly_return", ascending=False).head(10).reset_index(drop=True)
    st.subheader("Top 10 Green Stocks:")
    
    fig, ax = plt.subplots()
    ax.bar(top_10_green_stocks["Ticker"], top_10_green_stocks["yearly_return"])
    ax.set_xlabel("Stocks")
    ax.set_ylabel("Yearly Return (%)")
    ax.set_title("Top 10 Green Stocks")
    plt.xticks(rotation=45)
    ax.bar_label(ax.containers[0], fontsize=7, padding=3)
    st.pyplot(fig)
    
    with st.expander("Click here for insights on the top 10 green stocks"):
        st.write("**1. TRENT is the top performing green stock:** With a yearly return of 223.093%, TRENT significantly outperforms other green stocks in the top 10 list.")
        st.write("**2. Significant drop after TRENT:** There is a large gap in yearly return between TRENT and the next highest performing stock (BEL at 101.76%).")
        st.write("**3. Majority of stocks have positive returns:** All listed stocks show positive yearly returns, indicating a generally positive performance of green stocks.")
        st.write("**4. Range of returns:** The yearly returns range from a high of 223.093% (TRENT) to a low of 53.2574% (HCLTECH) within the top 10.")
        st.write("**5. Clustering in lower returns:** A cluster of stocks (BHARTIARTL, POWERGRID, BPCL, HEROMOTOCO, SUNPHARMA, HCLTECH) show yearly returns in a narrower range (around 50-70%).")
        
    
    #st.write(top_10_green_stocks)
    
    #Top 10 Loss Stocks: Sort the stocks based on their yearly return and select the bottom 10.
    st.subheader("Top 10 Loss Stocks")
    top_10_low_stocks = stock_returns.sort_values(by="yearly_return", ascending=True).head(10).reset_index(drop=True)
    
    fig, ax = plt.subplots()
    ax.bar(top_10_low_stocks["Ticker"], top_10_low_stocks["yearly_return"])
    ax.set_xlabel("Stocks")
    ax.set_ylabel("Yearly Return (%)")
    ax.set_title("Top 10 Loss Stocks")
    plt.xticks(rotation=45)
    ax.bar_label(ax.containers[0], fontsize=7, padding=3)
    st.pyplot(fig)
    
    with st.expander("Click here for insights on the top 10 loss stocks"):
        st.write("**1. TATASTEEL is the worst performing stock:** With a yearly return of -33.33%, TATASTEEL is the worst performing stock in the top 10 loss stocks list.")
        st.write("**2. Significant drop after TATASTEEL:** There is a large gap in yearly return between TATASTEEL and the next lowest performing stock (JSWSTEEL at -22.22%).")
        st.write("**3. Majority of stocks have negative returns:** All listed stocks show negative yearly returns, indicating a generally negative performance of loss stocks.")
        st.write("**4. Range of returns:** The yearly returns range from a low of -33.33% (TATASTEEL) to a high of -22.22% (JSWSTEEL) within the top 10.")
        st.write("**5. Clustering in lower returns:** A cluster of stocks (HDFCLIFE, TITAN, HINDALCO, NTPC, JSWSTEEL) show yearly returns in a narrower range (around -22% to -23%).")
    
    #Market Summary:
    st.subheader("Market Summary")
    st.write("The market summary provides an overview of the stock market data. The summary includes the overall number of green vs. red stocks, the average price across all stocks, and the average volume across all stocks.")
    st.subheader("Calculation the overall number of green vs. red stocks")
    green_stocks = stock_returns[stock_returns["yearly_return"] > 0]
    red_stocks = stock_returns[stock_returns["yearly_return"] < 0]
    st.write(f"**Number of Green Stocks:** {green_stocks.shape[0]}")
    st.dataframe(green_stocks, width=1000, hide_index=True)
    st.write(f"**Number of Red Stocks:** {red_stocks.shape[0]}")
    st.dataframe(red_stocks, width=1000, hide_index=True)
    
    st.subheader("Calculation of the average price across all stocks")
    average_price = all_data_df.groupby('Ticker')["close"].mean()
    col1, col2= st.columns(2)
    with col1:
        st.dataframe(average_price, width=250)
    with col2: 
        with st.expander("Key Points", expanded=True):
            st.write("**1. Average price range:** The average price of stocks ranges from a low of 1.0 (ADANIPORTS) to a high of 1,000.0 (TITAN).")
            st.write("**2. Clustering in lower average prices:** A cluster of stocks (ADANIPORTS, ASIANPAINT, AXISBANK, BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV) have average prices in a narrower range (around 1.0 to 2.0).")
            st.write("**3. Clustering in higher average prices:** A cluster of stocks (TITAN, TCS, TECHM, SUNPHARMA, SHREECEM, SBIN) have average prices in a narrower range (around 500.0 to 1,000.0).")
    
    st.subheader("Calculation of the average volume across all stocks")
    average_volume = all_data_df.groupby('Ticker')["volume"].mean()
    col1, col2= st.columns(2)
    with col1:
        st.dataframe(average_volume, width=250)
    with col2:
        with st.expander("Key Points", expanded=True):
            st.write("**1. Average volume range:** The average volume of stocks ranges from a low of 1.0 (ADANIPORTS) to a high of 1,000.0 (TITAN).")
            st.write("**2. Clustering in lower average volumes:** A cluster of stocks (ADANIPORTS, ASIANPAINT, AXISBANK, BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV) have average volumes in a narrower range (around 1.0 to 2.0).")
            st.write("**3. Clustering in higher average volumes:** A cluster of stocks (TITAN, TCS, TECHM, SUNPHARMA, SHREECEM, SBIN) have average volumes in a narrower range (around 500.0 to 1,000.0).")



except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Closing the connection after the operation is complete
    conn.close()
    print("Connection closed successfully.")

