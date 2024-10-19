# E-commerce Data Analytics Dashboard 📊

This project is an E-commerce dashboard built with Streamlit, allowing users to explore various data metrics, trends, and visualizations of order data. It includes insights into total orders, revenue, product trends, and more.

## Table of Contents
- [E-commerce Data Analytics Dashboard 📊](#e-commerce-data-analytics-dashboard-)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [Running the App Locally](#running-the-app-locally)
  - [Deployed Version](#deployed-version)

## Prerequisites
- Python 3.9 or higher
- `pip` (Python package manager)

## Installation and Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yosriku/Data-Analytics-Dashboard.git
    cd Data-Analytics-Dashboard
    ```

2. **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Place the dataset files** in the appropriate folder:
   Ensure you have the following CSV files in the specified path:
   - `olist_orders_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_products_dataset.csv`
   - `olist_customers_dataset.csv`
   - `olist_order_reviews_dataset.csv`
   
   Adjust the paths in the script if necessary.

## Running the App Locally

1. **Run the Streamlit app**:
    ```bash
    streamlit run dashboard.py
    ```

2. **Open the app**:
   - After running the command above, Streamlit will provide a URL (usually `http://localhost:8501`).
   - Open the URL in your web browser to access the dashboard.

## Deployed Version
The dashboard has been deployed and is accessible online:

[https://data-analytics-dashboard-dicoding.streamlit.app/](https://data-analytics-dashboard-dicoding.streamlit.app/)

Feel free to explore the data and insights directly on the deployed version!

