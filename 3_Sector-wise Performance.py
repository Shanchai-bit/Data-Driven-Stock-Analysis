import streamlit as st
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.header("Sector-wise Performance")
st.write('**Average Yearly Return by Sector:** A bar chart where each bar represents a sector and its height indicates the average yearly return for stocks within that sector')
# Establishing a connection to the MySQL database using SQLAlchemy engine
engine = create_engine("mysql+mysqldb://root:shan@localhost:3306/data_driven_stock_analysis")  # root@localhost:3306
try:
    # Connecting to the database engine
    conn = engine.connect()
    
    # Execute SQL query and load data into a Pandas DataFrame
    df_stock = pd.read_sql('SELECT * FROM data_driven_stock_analysis.combined_data;', conn)
    
except Exception as e:
    st.write("Error: ", e)
finally:
    # Close the connection
    conn.close()

df_sector = pd.read_csv(r"D:\Guvi_Project\DD_Stock_Analysis\Data_Folder\Sector_data - Sheet1.csv")

# Extract ticker symbols from sector data
df_sector[['Company_Name', 'Ticker_Symbol']] = df_sector['Symbol'].str.split(': ', expand=True)

# Merge stock data with sector data
merged_data = df_stock.merge(df_sector, left_on='Ticker', right_on='Ticker_Symbol', how='left')

# Convert date to datetime and extract year
merged_data['date'] = pd.to_datetime(merged_data['date'])
merged_data['year'] = merged_data['date'].dt.year

# Calculate yearly return
merged_data['yearly_return'] = ((merged_data['close'] - merged_data['open']) / merged_data['open']) * 100

# Compute sector-wise average yearly return
sector_performance = (merged_data.groupby('sector')['yearly_return']
                      .mean()
                      .reset_index()
                      .sort_values(by='yearly_return', ascending=False))


# Plot bar chart
# Create a figure
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='yearly_return', y='sector', data=sector_performance, palette='coolwarm')
plt.xlabel("Average Yearly Return (%)")
plt.ylabel("Sector")
plt.title("Average Yearly Return by Sector")
plt.show()

st.pyplot(fig)

with st.expander("Sector-wise peformance insights"):
    st.write("**1. Software and Retailing Lead the Pack:** The chart clearly shows that the Software and Retailing sectors have the highest average yearly returns.  They stand out significantly from the rest, indicating strong growth and profitability in these areas. This suggests that investments in these sectors have historically yielded the best results on average.")
    st.write("**2. Mining Sector Severely Underperforms:**  At the opposite end of the spectrum, the Mining sector exhibits the worst average yearly return, dipping significantly into negative territory. This indicates substantial challenges or unfavorable market conditions affecting the mining industry during the observed period.")
    st.write("**3. Wide Range of Performance Across Sectors:**  The chart illustrates a wide dispersion of average yearly returns across different sectors. This highlights the importance of sector allocation in investment strategies, as choosing the right sectors can significantly impact overall portfolio performance. The difference between the top performers (Software, Retailing) and the laggard (Mining) is substantial.")
    st.write("**4. Concentration of Negative Returns:**  A significant portion of the sectors (Aluminum, Steel, Food & Tobacco, Defence, Energy, Paints, Finance, Miscellaneous, Pharmaceuticals, Engineering, Insurance, Banking, Cement, Power, Automobiles, FMCG, and Textiles) show negative or near-zero average yearly returns. This suggests broader economic challenges or sector-specific headwinds affecting a wide range of industries.")
    st.write("**5. Potential for Sector-Specific Analysis:**  The chart provides a high-level overview of sector performance. However, it also suggests the need for deeper sector-specific analysis.  For example, understanding the factors driving the strong performance of Software and Retailing or the challenges facing the Mining sector would require further investigation into industry trends, competitive landscapes, regulatory environments, and macroeconomic factors.")
