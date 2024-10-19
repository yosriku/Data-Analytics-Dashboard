import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

base_dir = os.path.dirname(__file__)

@st.cache_data
def load_data():
    orders = pd.read_csv(base_dir+'/dataset/olist_orders_dataset.csv')
    order_items = pd.read_csv(base_dir+'/dataset/olist_order_items_dataset.csv')
    products = pd.read_csv(base_dir+'/dataset/olist_products_dataset.csv')
    customers = pd.read_csv(base_dir+'/dataset/olist_customers_dataset.csv')
    sellers = pd.read_csv(base_dir+'/dataset/olist_sellers_dataset.csv')
    geolocation = pd.read_csv(base_dir+'/dataset/olist_geolocation_dataset.csv')
    reviews = pd.read_csv(base_dir+'/dataset/olist_order_reviews_dataset.csv')

    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    return orders, order_items, products, customers, sellers, geolocation, reviews

orders, order_items, products, customers, sellers, geolocation, reviews = load_data()

st.sidebar.header("Filters")
min_date = orders["order_purchase_timestamp"].min()
max_date = orders["order_purchase_timestamp"].max()

start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])

if st.sidebar.button("Cancel Filter"):
    start_date = min_date
    end_date = max_date

filtered_orders = orders[(orders["order_purchase_timestamp"] >= pd.Timestamp(start_date)) &
                         (orders["order_purchase_timestamp"] <= pd.Timestamp(end_date))]

total_orders = filtered_orders['order_id'].nunique()
total_revenue = order_items['price'].sum()
avg_order_value = order_items.groupby('order_id')['price'].sum().mean()

st.title("E-commerce Dashboard 📊")
st.subheader("Performance Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Avg. Order Value", f"${avg_order_value:,.2f}")

st.subheader("Daily Orders Trend")
daily_orders = filtered_orders.resample('D', on='order_purchase_timestamp')['order_id'].nunique()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_orders.index, daily_orders.values, marker='o', color='tab:blue')
ax.set_title("Number of Orders per Day")
ax.set_xlabel("Date")
ax.set_ylabel("Orders")
st.pyplot(fig)

st.subheader("Top 5 Best Performing Products")
merged_data = pd.merge(order_items, products, on='product_id')
top_products = merged_data.groupby('product_category_name')['price'].sum().nlargest(5)

fig, ax = plt.subplots(figsize=(8, 4))
top_products.plot(kind='barh', ax=ax, color='tab:green')
ax.set_title("Top 5 Products by Revenue")
ax.set_xlabel("Revenue")
st.pyplot(fig)

st.subheader("Customer State Distribution")
customer_state_counts = customers['customer_state'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8, 4))
customer_state_counts.plot(kind='bar', ax=ax, color='tab:purple')
ax.set_title("Top 10 States by Customer Count")
ax.set_xlabel("State")
ax.set_ylabel("Number of Customers")
st.pyplot(fig)

st.subheader("RFM Analysis")

recency = (orders['order_purchase_timestamp'].max() - orders.groupby('customer_id')['order_purchase_timestamp'].max()).dt.days
frequency = orders.groupby('customer_id')['order_id'].nunique()
monetary = pd.merge(orders, order_items, on='order_id').groupby('customer_id')['price'].sum()

rfm = pd.DataFrame({
    'Recency': recency,
    'Frequency': frequency,
    'Monetary': monetary
})

rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=range(4, 0, -1))
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=range(1, 5))
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=range(1, 5))
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

rfm_heatmap = rfm.groupby(['R_Score', 'F_Score'])['Monetary'].mean().unstack()
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(rfm_heatmap, cmap='YlGnBu', annot=True, fmt='.0f', ax=ax)
ax.set_title('RFM Segmentation Heatmap')
st.pyplot(fig)

# Bar chart for total customers and sellers by state
st.subheader("Total Number of Customers and Sellers by State")

customer_state_counts = customers['customer_state'].value_counts().reset_index()
customer_state_counts.columns = ['state', 'num_customers']

seller_state_counts = sellers['seller_state'].value_counts().reset_index()
seller_state_counts.columns = ['state', 'num_sellers']

state_counts = pd.merge(customer_state_counts, seller_state_counts, on='state', how='outer').fillna(0)
state_counts = state_counts.sort_values(by='num_customers', ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
state_counts.plot(x='state', y=['num_customers', 'num_sellers'], kind='bar', ax=ax)

ax.set_title("Total Number of Customers and Sellers by State")
ax.set_xlabel("State")
ax.set_ylabel("Number of Customers and Sellers")
st.pyplot(fig)

st.subheader("Scatter Plot: Harga Produk vs Biaya Pengiriman")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=order_items, x='price', y='freight_value', alpha=0.5, ax=ax)
ax.set_title("Harga vs Biaya Pengiriman")
ax.set_xlabel("Harga Produk (Rp)")
ax.set_ylabel("Biaya Pengiriman (Rp)")
st.pyplot(fig)

st.subheader("Distribusi Skor Ulasan")
fig, ax = plt.subplots(figsize=(8, 4))
sns.countplot(data=reviews, x='review_score', palette='Blues', ax=ax)
ax.set_title("Distribusi Skor Ulasan")
ax.set_xlabel("Skor Ulasan")
ax.set_ylabel("Jumlah Ulasan")
st.pyplot(fig)

orders['year_month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)
monthly_orders = orders.groupby('year_month').size().reset_index(name='order_count')
monthly_orders['year_month'] = pd.to_datetime(monthly_orders['year_month'], format='%Y-%m')

st.subheader("Tren Jumlah Pesanan per Bulan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_orders, x='year_month', y='order_count', marker='o', ax=ax)
ax.set_title("Tren Jumlah Pesanan per Bulan")
ax.set_xlabel("Tahun-Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)
