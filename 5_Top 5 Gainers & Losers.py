import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.header("Top 2 Gainers and Losers")
st.write('**Top 5 Gainers and Losers by Month:** Create a set of 12 bar charts for each month showing the top 5 gainers and losers based on percentage return.')
# Establishing a connection to the MySQL database using SQLAlchemy engine
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")  # root@localhost:3306
try:
    # Connecting to the database engine
    conn = engine.connect()
    
    # Execute SQL query and load data into a Pandas DataFrame
    stock_data = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)
    
except Exception as e:
    st.write("Error: ", e)
finally:
    # Close the connection
    conn.close()
    
# Convert date to datetime and extract year and month
stock_data['date'] = pd.to_datetime(stock_data['date'])
stock_data['year'] = stock_data['date'].dt.year
stock_data['month'] = stock_data['date'].dt.month

# Calculate monthly returns
monthly_returns = stock_data.groupby(['year', 'month', 'Ticker'])[['open', 'close']].last()
monthly_returns['monthly_return'] = ((monthly_returns['close'] - monthly_returns['open']) / monthly_returns['open']) * 100
monthly_returns.reset_index(inplace=True)

# Plot monthly top 5 gainers and losers
for (year, month), group in monthly_returns.groupby(['year', 'month']):
    top_gainers = group.nlargest(5, 'monthly_return')
    top_losers = group.nsmallest(5, 'monthly_return')
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.barplot(x='monthly_return', y='Ticker', data=top_gainers, ax=axes[0], palette='Greens')
    axes[0].set_title(f"Top 5 Gainers - {year}-{month}")
    
    sns.barplot(x='monthly_return', y='Ticker', data=top_losers, ax=axes[1], palette='Reds')
    axes[1].set_title(f"Top 5 Losers - {year}-{month}")
    
    plt.tight_layout()
    st.pyplot(fig)