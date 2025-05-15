# Biotech Stock Dashboard

This project is a data pipeline and Streamlit dashboard that collects, processes, and visualizes stock data for select biotech companies using the [Alpha Vantage API](https://www.alphavantage.co/).

##  Overview

This application focuses on extracting and analyzing stock and company overview data for biotech companies like Argenx (ARGX) and Genmab (GMAB). The workflow includes:

-  **Extracting** data via Alpha Vantage API (daily stock prices and company overview)
-  **Transforming** it using pandas (cleaning and normalizing)
-  **Loading** it into a PostgreSQL database
-  **Visualizing** it using Streamlit:
  - A **Stock Details** page showing trends for a single company
  - A **Comparison** page to compare metrics between companies

---

##  Tech Stack

- Python (ETL logic, Streamlit)
- Pandas (data cleaning/transformation)
- SQLAlchemy & psycopg2 (PostgreSQL integration)
- PostgreSQL (data storage)
- Streamlit (frontend dashboard)
- Alpha Vantage API (financial data)

---

##  ETL Pipeline Details

###  Extraction

- Daily stock prices per company via Alpha Vantage's `TIME_SERIES_DAILY_ADJUSTED` endpoint
- Company overview details via Alpha Vantage's `OVERVIEW` endpoint

###  Transformation

- Clean and format numeric values (`market_cap`, `high`, `low`, etc.)
- Normalize structure for PostgreSQL
  - Overview data is **replaced** (Work in progress)
  - Daily stock data is **appended** (new rows only)

###  Load

Data is inserted into the following PostgreSQL tables:

- `company_overviews`: General static information (replaced on update)
- `daily_stock_argx`, `daily_stock_gmab`, etc.: Daily prices (high, low, date, etc.)

---

##  Streamlit App

The dashboard includes two main pages:

1. **Stock Details Page**  
   Explore stock trends, prices, and company overview for a selected company.

2. **Comparison Page**  
   Compare key metrics (e.g., high/low stock price, market cap) across multiple biotech companies.

---

##  Data Flow Diagram (Mermaid)
TO BE ADDED: 
1 x diagram to show data normalisaiton 
1x diagram to show the flow of the ETL pipeline

README was generated using CHATGPT.

### Set up and run the ETL pipeline:
```bash
python3 -m scripts.run_etl
```

### Run Streamlit app locally:
```bash
streamlit run app/main.py
```

### Run all unit tests:
```bash
pytest
```

### Run a specific test file:
```bash
pytest tests/unittest/test_extract.py
```