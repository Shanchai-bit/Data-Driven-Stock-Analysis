import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Set Streamlit header and description
st.header("Top 2 Gainers and Losers")
st.write('**Top 5 Gainers and Losers by Month:** Create a set of 12 bar charts for each month showing the top 5 gainers and losers based on percentage return.')

# Establish a connection to the MySQL database using SQLAlchemy engine
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")

try:
    # Connecting to the database engine
    conn = engine.connect()
    
    # Execute SQL query and load data into a Pandas DataFrame
    stock_data = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)
    
    # Convert date column to datetime format and extract year and month for grouping
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    stock_data['year'] = stock_data['date'].dt.year
    stock_data['month'] = stock_data['date'].dt.month

    # Calculate monthly returns
    # Group data by year, month, and ticker, selecting the last available open and close prices
    monthly_returns = stock_data.groupby(['year', 'month', 'Ticker'])[['open', 'close']].last()

    # Compute the percentage return for each stock in the month
    monthly_returns['monthly_return'] = ((monthly_returns['close'] - monthly_returns['open']) / monthly_returns['open']) * 100

    # Reset index to bring year, month, and ticker back as columns
    monthly_returns.reset_index(inplace=True)

    # Define local output directory for storing the monthly returns CSV file
    output_dir = r"D:\Guvi_Project\DD_Stock_Analysis\Data_Folder\Visualizations"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    # Save the monthly returns data as a CSV file locally
    monthly_returns.to_csv(os.path.join(output_dir, "monthly_returns.csv"), index=False)

    # Load the saved CSV file and store it in the MySQL database
    monthly_returns = pd.read_csv(os.path.join(output_dir, "monthly_returns.csv"))
    monthly_returns.to_sql(name="monthly_returns", con=engine, index=False, if_exists='replace')

except Exception as e:
    # Handle and display errors in Streamlit
    st.write("Error: ", e)

finally:
    # Close the database connection
    conn.close()

# Plot monthly top 5 gainers and losers
# Loop through each unique year-month combination
for (year, month), group in monthly_returns.groupby(['year', 'month']):
    # Select the top 5 stocks with the highest percentage returns
    top_gainers = group.nlargest(5, 'monthly_return')
    
    # Select the bottom 5 stocks with the lowest percentage returns
    top_losers = group.nsmallest(5, 'monthly_return')

    # Create a side-by-side bar plot for gainers and losers
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot top 5 gainers
    sns.barplot(x='monthly_return', y='Ticker', data=top_gainers, ax=axes[0], palette='Greens')
    axes[0].set_title(f"Top 5 Gainers - {year}-{month}")

    # Plot top 5 losers
    sns.barplot(x='monthly_return', y='Ticker', data=top_losers, ax=axes[1], palette='Reds')
    axes[1].set_title(f"Top 5 Losers - {year}-{month}")

    # Adjust layout for better readability
    plt.tight_layout()

    # Display the bar charts in Streamlit
    st.pyplot(fig)
