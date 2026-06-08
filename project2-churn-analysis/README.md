Retail Sales Performance Analytics
This project is a complete end-to-end retail sales analysis built on the Sample Superstore dataset containing 9,994 orders across 2014 to 2017. It covers the full data analyst workflow — raw data ingestion, cleaning, feature engineering, exploratory analysis, visualisation, and automated professional PDF report generation. The goal was to turn messy transactional sales data into clear, actionable business insights that a non-technical executive can read and act on immediately.
Business Problem
A retail business with four years of sales data across three product categories, four regions, and three customer segments needed to understand why their overall profit margin was only 12.5% despite strong revenue growth. The analysis identifies which products, regions, and discount strategies are destroying profitability, and where to focus marketing and operational effort for maximum ROI.
Key Findings
The business generated $2,297,201 in total revenue with $286,397 in profit at a 12.5% margin. Year-over-year sales growth was strong at 20.4%, but 1,871 orders — 18.7% of all orders — were unprofitable. The West region was the strongest performer with $108,418 in profit, while the Central region needed immediate attention. The most critical finding was that heavy discounting above 41% generates negative average profit, meaning those orders were actively losing money. Technology produced the highest profit margin of all categories, while Furniture showed high sales volume but dangerously low margins — a clear pricing or cost issue. Q4 was consistently the strongest quarter across all four years.
What Was Built
The raw dataset was cleaned and enriched with over 10 engineered features including profit margin percentage per order, discount band classification (No Discount, Low 1–20%, Medium 21–40%, High 41%+), a boolean flag for unprofitable orders, calculated shipping time, shipping speed classification, and a data quality flag. The final deliverable is a master dashboard showing multi-year monthly sales trends, category profitability heatmap by quarter, segment breakdown, and regional comparison — plus an automatically generated PDF business report with executive summary, KPI page, and prioritised recommendations.
Tools Used
Python 3, Pandas, Matplotlib, Seaborn, NumPy, ReportLab for PDF generation, and Jupyter Notebook.
Business Recommendations
The analysis recommends capping maximum discounts at 20% since data shows anything above this destroys profitability. Marketing budget should shift toward Technology products which generate the highest return per sales dollar. Furniture pricing needs investigation as the high volume but low margin combination signals a cost or pricing problem. Q4 inventory and promotions should be increased since it is the peak season across all categories every year. A customer loyalty programme targeting the Consumer segment would have the highest revenue impact.
How to Run
Clone the repository and install dependencies with pip install pandas matplotlib seaborn numpy reportlab jupyter. Open day2.ipynb for the full analysis and Day3_PDF_Report.ipynb to regenerate the automated business report.

Built by Gurleen Saini — Data Analyst specialising in business intelligence, sales analytics, and automated reporting.
Contact: gurleensainitamber15@gmail.com
GitHub: https://github.com/gurleensainitamber15
Available for freelance data analytics projects. If you need sales analytics, dashboards, or automated reporting for your business — let's connect.
