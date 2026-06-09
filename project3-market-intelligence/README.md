# Project 3 - Market Intelligence Dashboard

Live Market Intelligence Dashboard
A production-ready, live market intelligence dashboard that continuously monitors product pricing, competitor comparisons, stock levels, and brand competitiveness across 100 products — and surfaces automated alerts when action is needed. The dashboard is deployed live and accessible directly in the browser without any installation.
Live Dashboard: https://ollbxkgy976jdgg5xjywbl.streamlit.app/
Business Problem
E-commerce and retail businesses lose sales every day because their prices are higher than competitors and they don't know it, products go out of stock with no one getting alerted, brand managers have no single view of their competitive position, and price trend data is scattered across spreadsheets with no automation. This dashboard solves all four problems in one place, giving any business a real-time competitive intelligence system they can check every morning in their browser.
What the Dashboard Does
The dashboard tracks 100 products across five categories — Laptops, Smartphones, Tablets, Headphones, and Cameras — covering 19 brands including Apple, Sony, Samsung, Lenovo, HP, Dell, Xiaomi, Bose, Sennheiser, and more. For every product it shows the current price versus competitor price, a competitiveness score from 0 to 100, stock status, and an automated alert. The four alert types are COMPETITOR CHEAPER (price above competitor — action needed), LOW STOCK (inventory running low — restock soon), OUT OF STOCK (urgent restock required), and OK (price competitive and stock healthy).
The brand analysis section shows aggregate metrics per brand including average price, average rating, total reviews, overall competitiveness score, and how many products are priced below the competitor. The category intelligence section shows price ranges (minimum, maximum, average) per category, average discount percentage, out-of-stock count, and average customer rating. The price history section shows a 7-day price trend per product with competitor price overlaid, making it easy to spot pricing volatility and opportunity windows.
Technical Architecture
The project has two components. The data collection pipeline (built in Jupyter Notebook) scrapes and processes product data, calculates all metrics and scores, generates alerts, and stores everything in a SQLite database and CSV files. The Streamlit dashboard reads from these data sources and renders the live interface with interactive filters, charts, and tables. The SQLite database stores the full price history enabling trend analysis over time.
Tools Used
Python 3, Streamlit for the live web dashboard, Pandas for data processing and analysis, SQLite for price history storage, Matplotlib and Plotly for interactive charts, openpyxl for Excel export, and Jupyter Notebook for the data collection pipeline.
Business Use Cases
This dashboard architecture can be adapted for D2C brands monitoring Amazon or Flipkart competitor pricing, retail chains tracking category-level price positioning, e-commerce managers getting daily alerts on pricing gaps, brand managers measuring competitive standing across all SKUs, and procurement teams identifying the best vendor pricing windows.
How to Run Locally
Clone the repository and install dependencies with pip install streamlit pandas matplotlib plotly openpyxl jupyter. Run streamlit run streamlit_app.py and the dashboard opens automatically at http://localhost:8501. To refresh the data first, run the Day7_Data_Collection.ipynb notebook which will update all CSV files and the SQLite database before launching the dashboard.

Built by Gurleen Saini — Data Analyst specialising in live dashboards, competitive intelligence, and business analytics.
Contact: gurleensainitamber15@gmail.com
GitHub: https://github.com/gurleensainitamber15
Available for freelance dashboard and analytics projects. If your business needs a live competitive intelligence system, pricing tracker, or automated reporting dashboard — let's connect.
