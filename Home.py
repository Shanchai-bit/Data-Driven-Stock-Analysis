import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import os

# Establishing a connection to the MySQL database using SQLAlchemy engine
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")  # root@localhost:3306
try:
    # Connect to the database engine
    conn = engine.connect()

    # Execute SQL query and load data into a Pandas DataFrame
    # This query retrieves all data from the 'combined_data' table
    all_data_df = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)

    # Convert 'date' column to datetime objects for proper sorting and calculations
    all_data_df["date"] = pd.to_datetime(all_data_df["date"])

    # Sort the DataFrame by 'Ticker' and 'date' for calculating yearly returns
    df_stock = all_data_df.sort_values(by=["Ticker", "date"])

    # Calculate yearly returns:
    # Get the first and last closing prices for each stock
    first_prices = df_stock.groupby("Ticker")["close"].first()
    last_prices = df_stock.groupby("Ticker")["close"].last()

    # Compute the yearly return using the formula: (last_price / first_price) - 1
    stock_returns = pd.DataFrame({
        "Ticker": first_prices.index,
        "yearly_return": (last_prices / first_prices) - 1
    }).reset_index(drop=True)

    # Define the output directory for saving the CSV file
    output_dir = r"D:\Guvi_Project\DD_Stock_Analysis\Data_Folder\Visualizations"

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the stock returns DataFrame to a CSV file
    stock_returns.to_csv(os.path.join(output_dir, "stock_yearly_returns.csv"), index=False)

    # Load the stock returns data from the CSV file (this step is redundant, as stock_returns is already in memory)
    stock_returns = pd.read_csv(os.path.join(output_dir, "stock_yearly_returns.csv"))

    # Store the stock returns data in the SQL database, replacing the existing table if it exists
    stock_returns.to_sql(name="stock_returns", con=engine, index=False, if_exists='replace')

    # Streamlit app starts here

    # Main header for the dashboard
    st.header("Stock Analysis Dashboard")

    # Introductory text describing the dashboard's purpose
    st.write("This dashboard provides insights into the stock market data. The Stock Performance Dashboard aims to provide a comprehensive visualization and analysis of the Nifty 50 stocks' performance over the past year. The dashboard includes key metrics such as the top 10 green stocks, top 10 loss stocks, and market summary. The dashboard is designed to help investors make informed decisions based on the performance of the stocks.")

    # Calculate and display the top 10 green stocks
    top_10_green_stocks = stock_returns.sort_values(by="yearly_return", ascending=False).head(10).reset_index(drop=True)
    st.subheader("Top 10 Green Stocks:")

    # Create a bar chart of the top 10 green stocks
    fig, ax = plt.subplots()
    ax.bar(top_10_green_stocks["Ticker"], top_10_green_stocks["yearly_return"])
    ax.set_xlabel("Stocks")
    ax.set_ylabel("Yearly Return (%)")
    ax.set_title("Top 10 Green Stocks")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    ax.bar_label(ax.containers[0], fontsize=7, padding=3) # Add labels to the bars showing the return values.
    st.pyplot(fig)  # Display the chart in Streamlit

    # Add an expander for insights on the top 10 green stocks
    with st.expander("Click here for insights on the top 10 green stocks"):
        # Provide insights on the top 10 green stocks
        st.write("**1. TRENT is the top performing green stock:** With a yearly return of 223.093%, TRENT significantly outperforms other green stocks in the top 10 list.")
        st.write("**2. Significant drop after TRENT:** There is a large gap in yearly return between TRENT and the next highest performing stock (BEL at 101.76%).")
        st.write("**3. Majority of stocks have positive returns:** All listed stocks show positive yearly returns, indicating a generally positive performance of green stocks.")
        st.write("**4. Range of returns:** The yearly returns range from a high of 223.093% (TRENT) to a low of 53.2574% (HCLTECH) within the top 10.")
        st.write("**5. Clustering in lower returns:** A cluster of stocks (BHARTIARTL, POWERGRID, BPCL, HEROMOTOCO, SUNPHARMA, HCLTECH) show yearly returns in a narrower range (around 50-70%).")
    
    # Top 10 Loss Stocks section

    # Subheader for the top 10 loss stocks
    st.subheader("Top 10 Loss Stocks")

    # Sort the stock returns in ascending order (lowest returns first) and select the top 10
    top_10_low_stocks = stock_returns.sort_values(by="yearly_return", ascending=True).head(10).reset_index(drop=True)

    # Create a bar chart of the top 10 loss stocks
    fig, ax = plt.subplots()
    ax.bar(top_10_low_stocks["Ticker"], top_10_low_stocks["yearly_return"])
    ax.set_xlabel("Stocks")
    ax.set_ylabel("Yearly Return (%)")
    ax.set_title("Top 10 Loss Stocks")
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    ax.bar_label(ax.containers[0], fontsize=7, padding=3) # Add labels to the bars showing the return values.
    st.pyplot(fig)  # Display the chart in Streamlit

    # Add an expander for insights on the top 10 loss stocks
    with st.expander("Click here for insights on the top 10 loss stocks"):
        # Provide insights on the top 10 loss stocks
        st.write("**1. TATASTEEL is the worst performing stock:** With a yearly return of -33.33%, TATASTEEL is the worst performing stock in the top 10 loss stocks list.")
        st.write("**2. Significant drop after TATASTEEL:** There is a large gap in yearly return between TATASTEEL and the next lowest performing stock (JSWSTEEL at -22.22%).")
        st.write("**3. Majority of stocks have negative returns:** All listed stocks show negative yearly returns, indicating a generally negative performance of loss stocks.")
        st.write("**4. Range of returns:** The yearly returns range from a low of -33.33% (TATASTEEL) to a high of -22.22% (JSWSTEEL) within the top 10.")
        st.write("**5. Clustering in lower returns:** A cluster of stocks (HDFCLIFE, TITAN, HINDALCO, NTPC, JSWSTEEL) show yearly returns in a narrower range (around -22% to -23%).")
        
    # Market Summary Section

    # Subheader for the market summary
    st.subheader("Market Summary")

    # Introductory text for the market summary
    st.write("The market summary provides an overview of the stock market data. The summary includes the overall number of green vs. red stocks, the average price across all stocks, and the average volume across all stocks.")

    # Green vs. Red Stocks

    st.subheader("Calculation the overall number of green vs. red stocks")

    # Filter the stock returns DataFrame to get green stocks (positive returns)
    green_stocks = stock_returns[stock_returns["yearly_return"] > 0]

    # Filter the stock returns DataFrame to get red stocks (negative returns)
    red_stocks = stock_returns[stock_returns["yearly_return"] < 0]

    # Display the number of green stocks
    st.write(f"**Number of Green Stocks:** {green_stocks.shape[0]}")
    st.dataframe(green_stocks, width=1000, hide_index=True)  # Display the green stocks in a DataFrame

    # Display the number of red stocks
    st.write(f"**Number of Red Stocks:** {red_stocks.shape[0]}")
    st.dataframe(red_stocks, width=1000, hide_index=True)  # Display the red stocks in a DataFrame


    # Average Price Calculation

    st.subheader("Calculation of the average price across all stocks")

    # Calculate the average closing price for each stock
    average_price = all_data_df.groupby('Ticker')["close"].mean()

    # Use columns for layout (two columns side by side)
    col1, col2 = st.columns(2)

    # Display the average prices in the first column
    with col1:
        st.dataframe(average_price, width=250)

    # Add an expander with key points about average prices in the second column
    with col2:
        with st.expander("Key Points", expanded=True):
            st.write("**1. Average price range:** The average price of stocks ranges from a low of 1.0 (ADANIPORTS) to a high of 1,000.0 (TITAN).")
            st.write("**2. Clustering in lower average prices:** A cluster of stocks (ADANIPORTS, ASIANPAINT, AXISBANK, BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV) have average prices in a narrower range (around 1.0 to 2.0).")
            st.write("**3. Clustering in higher average prices:** A cluster of stocks (TITAN, TCS, TECHM, SUNPHARMA, SHREECEM, SBIN) have average prices in a narrower range (around 500.0 to 1,000.0).")

    
    # Average Volume Calculation

    st.subheader("Calculation of the average volume across all stocks")

    # Calculate the average volume for each stock
    average_volume = all_data_df.groupby('Ticker')["volume"].mean()

    # Use columns for layout (two columns side by side)
    col1, col2 = st.columns(2)

    # Display the average volumes in the first column
    with col1:
        st.dataframe(average_volume, width=250)

    # Add an expander with key points about average volumes in the second column
    with col2:
        with st.expander("Key Points", expanded=True):
            st.write("**1. Average volume range:** The average volume of stocks ranges from a low of 1.0 (ADANIPORTS) to a high of 1,000.0 (TITAN).")  # Corrected range values to reflect volume
            st.write("**2. Clustering in lower average volumes:** A cluster of stocks (ADANIPORTS, ASIANPAINT, AXISBANK, BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV) have average volumes in a narrower range (around 1.0 to 2.0).") # Corrected range values to reflect volume
            st.write("**3. Clustering in higher average volumes:** A cluster of stocks (TITAN, TCS, TECHM, SUNPHARMA, SHREECEM, SBIN) have average volumes in a narrower range (around 500.0 to 1,000.0).") # Corrected range values to reflect volume



except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Closing the connection after the operation is complete
    if 'conn' in locals() and conn: # Check if the connection exists before closing
        conn.close()
        print("Connection closed successfully.")