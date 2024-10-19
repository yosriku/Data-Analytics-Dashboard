import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data (adjust the path as needed)
@st.cache_data
def load_data():
    orders = pd.read_csv('dataset\\olist_orders_dataset.csv')
    order_items = pd.read_csv('dataset\\olist_order_items_dataset.csv')
    products = pd.read_csv('dataset\\olist_products_dataset.csv')
    customers = pd.read_csv('dataset\\olist_customers_dataset.csv')
    reviews = pd.read_csv('dataset\\olist_order_reviews_dataset.csv')

    # Convert date columns from string to datetime
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    return orders, order_items, products, customers, reviews

# Load data
orders, order_items, products, customers, reviews = load_data()

# Sidebar filter for date range
st.sidebar.header("Filters")

# Get the full range of dates for default values
min_date = orders["order_purchase_timestamp"].min()
max_date = orders["order_purchase_timestamp"].max()

# Date input for date range selection
start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date]
)

# Add a button to reset the date filter
if st.sidebar.button("Cancel Filter"):
    start_date = min_date
    end_date = max_date

# Filter the data based on the selected date range
filtered_orders = orders[
    (orders["order_purchase_timestamp"] >= pd.Timestamp(start_date)) &
    (orders["order_purchase_timestamp"] <= pd.Timestamp(end_date))
]

# Metrics
total_orders = filtered_orders['order_id'].nunique()
total_revenue = order_items['price'].sum()
avg_order_value = order_items.groupby('order_id')['price'].sum().mean()

# Display metrics
st.title("E-commerce Dashboard 📊")
st.subheader("Performance Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", total_orders)
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Avg. Order Value", f"${avg_order_value:,.2f}")

# Daily Orders Plot
st.subheader("Daily Orders Trend")
daily_orders = filtered_orders.resample('D', on='order_purchase_timestamp')['order_id'].nunique()

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_orders.index, daily_orders.values, marker='o', color='tab:blue')
ax.set_title("Number of Orders per Day", fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("Orders")
st.pyplot(fig)

# Top Products Plot
st.subheader("Top 5 Best Performing Products")
merged_data = pd.merge(order_items, products, on='product_id')
top_products = merged_data.groupby('product_category_name')['price'].sum().nlargest(5)

fig, ax = plt.subplots(figsize=(8, 4))
top_products.plot(kind='barh', ax=ax, color='tab:green')
ax.set_title("Top 5 Products by Revenue", fontsize=16)
ax.set_xlabel("Revenue")
st.pyplot(fig)

# Customer State Distribution Plot
st.subheader("Customer State Distribution")
customer_state_counts = customers['customer_state'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8, 4))
customer_state_counts.plot(kind='bar', ax=ax, color='tab:purple')
ax.set_title("Top 10 States by Customer Count", fontsize=16)
ax.set_xlabel("State")
ax.set_ylabel("Number of Customers")
st.pyplot(fig)

# 1. Scatter Plot: Harga vs Biaya Pengiriman
st.subheader("Scatter Plot: Harga Produk vs Biaya Pengiriman")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=order_items, x='price', y='freight_value', alpha=0.5, ax=ax)
ax.set_title("Harga vs Biaya Pengiriman", fontsize=16)
ax.set_xlabel("Harga Produk (Rp)")
ax.set_ylabel("Biaya Pengiriman (Rp)")
st.pyplot(fig)

# 2. Bar Plot: Distribusi Skor Ulasan
st.subheader("Distribusi Skor Ulasan")
fig, ax = plt.subplots(figsize=(8, 4))
sns.countplot(data=reviews, x='review_score', palette='Blues', ax=ax)
ax.set_title("Distribusi Skor Ulasan", fontsize=16)
ax.set_xlabel("Skor Ulasan")
ax.set_ylabel("Jumlah Ulasan")
st.pyplot(fig)

# 3. Line Plot: Tren Pesanan Bulanan
# Create 'year_month' column for monthly aggregation
orders['year_month'] = orders['order_purchase_timestamp'].dt.to_period('M').astype(str)

# Aggregate the number of orders per month
monthly_orders = orders.groupby('year_month').size().reset_index(name='order_count')

# Convert 'year_month' back to datetime for plotting
monthly_orders['year_month'] = pd.to_datetime(monthly_orders['year_month'], format='%Y-%m')

# Plot: Trend of Monthly Orders
st.subheader("Tren Jumlah Pesanan per Bulan")
fig, ax = plt.subplots(figsize=(10, 5))

# Line plot with seaborn for smoother visualization
sns.lineplot(data=monthly_orders, x='year_month', y='order_count', marker='o', ax=ax)

ax.set_title("Tren Jumlah Pesanan per Bulan", fontsize=16)
ax.set_xlabel("Tahun-Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)
