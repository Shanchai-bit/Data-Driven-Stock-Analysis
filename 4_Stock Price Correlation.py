import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.header("Stock Price Correlation")
st.write('**Stock Price Correlation Heatmap:** A heatmap to show the correlation between the closing prices of various stocks. Darker colors represent higher correlations.')
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
    
# Stock Price Correlation Analysis
# Pivot the data to have tickers as columns and dates as index
pivot_data = df.pivot(index='date', columns='Ticker', values='close')

# Calculate the correlation matrix
correlation_matrix = pivot_data.corr()

# Plot heatmap
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', linewidths=0.5)

# Add title
plt.title("Stock Price Correlation Heatmap")

# Display the heatmap
st.pyplot(fig)

with st.expander("Correlation insights"):
    st.write("**1. Self-Correlation (Diagonal):**  The diagonal line shows a perfect positive correlation (1.0) for each stock with itself. This is a given in any correlation matrix and simply confirms that a stock's price is perfectly correlated with its own price. It's a baseline for comparison.")
    st.write("**2. Clusters of High Correlation:**  Notice the prominent red blocks (indicating strong positive correlation) along the diagonal and in certain off-diagonal areas.  These clusters reveal groups of stocks whose prices tend to move together.  For example, the 'FINANCE' cluster (HDFCBANK, ICICIBANK, KOTAKBANK, SBIN, and others) shows strong internal correlations. This suggests shared factors influencing their price movements, like interest rates or overall financial market sentiment.")
    st.write("**3. Negative Correlations are Rare:**  The heatmap shows predominantly red and white/light shades, indicating mostly positive or weak/negligible correlations.  Blue regions, representing negative correlations, are scarce. This suggests that, generally, stocks in the Indian market tend to move in the same direction, though the strength of that movement varies.")
    st.write("**4. Potential for Diversification within Clusters:** While the \"FINANCE\" cluster shows high internal correlation, adding stocks from other clusters (like \"TECH\" or \"PHARMA\") with weaker correlations could enhance portfolio diversification.  Even within a cluster, variations in correlation strength exist. For instance, while most finance stocks are positively correlated, the degree of correlation varies, offering some room for nuanced diversification.")