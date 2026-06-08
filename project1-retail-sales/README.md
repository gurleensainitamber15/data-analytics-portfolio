 Retail Sales Performance Analytics
End-to-End Sales Analysis with Automated PDF Reporting | Python · Pandas · Matplotlib · Seaborn

 Project Overview
A complete retail sales analytics solution built on the Sample Superstore dataset (9,994 orders, 2014–2017). This project covers the full data analyst workflow — raw data ingestion, cleaning, feature engineering, exploratory analysis, visualisation, and automated professional PDF report generation.
The goal: turn messy transactional sales data into clear, actionable business insights that a non-technical executive can read and act on immediately.

Business Problem
A retail business with 4 years of sales data across 3 categories, 4 regions, and 3 customer segments needed to understand:

Why overall profit margin is only 12.5% despite strong revenue growth
Which products, regions, and discount strategies are destroying profitability
Where to focus marketing and operational effort for maximum ROI


Key Findings
MetricValueTotal Revenue$2,297,201Total Profit$286,397Profit Margin12.5%Unprofitable Orders1,871 (18.7%)YoY Sales Growth+20.4%Best RegionWest ($108,418 profit)

Heavy discounting (41%+) generates negative average profit — orders at this discount band are actively losing money
Technology has the highest profit margin despite not being the highest revenue category
Furniture shows high sales volume but dangerously low margins — a pricing or cost issue
Q4 is consistently the strongest quarter across all years and categories


 Technical Stack
ToolUsagePython 3Core languagePandasData cleaning, feature engineeringMatplotlib / SeabornData visualisationNumPyNumerical analysisReportLab / FPDFAutomated PDF report generationJupyter NotebookAnalysis environment

 Feature Engineering
Added 10+ calculated columns to the raw dataset:

Profit Margin % — per-order profitability
Discount Band — No Discount / Low (1–20%) / Medium (21–40%) / High (41%+)
Is Profitable — boolean flag for unprofitable order detection
Days to Ship — calculated shipping time
Shipping Speed — Normal / Slow / Fast classification
Order Year / Month / Quarter — time-based analysis dimensions
Revenue After Discount — actual revenue after discount applied
Data Quality Flag — Clean / Duplicate / Missing flagging


 Project Structure
retail-sales-analytics/

day2.ipynb                          # Main analysis notebook
Day3_PDF_Report.ipynb               # Automated PDF report generator
Sample_Superstore.csv               # Raw dataset (9,994 orders)
superstore_cleaned.csv              # Cleaned dataset with engineered feature                                               superstore_cleaned.xlsx             # Excel version of cleaned data
MASTER_DASHBOARD.png                # Full multi-chart dashboard
Superstore_Sales_Report.pdf         # Auto-generated business report
pdf_charts/                         # Individual chart exports

Visualisations Included

Monthly sales trend by year (2014–2017 overlaid)
Profit by category (Technology vs Furniture vs Office Supplies)
Sales by customer segment (Consumer / Corporate / Home Office)
Regional performance breakdown (West / East / Central / South)
Average profit per order by discount band
Profit heatmap: Category × Quarter
Top 10 loss-making products


 Business Recommendations

Cap maximum discount at 20% — data shows anything above this destroys profitability
Shift marketing toward Technology — highest return per sales dollar
Investigate Furniture pricing — high volume, low margin signals a cost or pricing problem
Increase Q4 inventory and promotions — peak season across all categories every year
Launch Consumer segment loyalty program — highest revenue driver


 How to Run
bash# Clone the repository
git clone https://github.com/gurleensainitamber15/data-analytics-portfolio.git
cd data-analytics-portfolio

# Install dependencies
pip install pandas matplotlib seaborn numpy reportlab jupyter

# Run the analysis
jupyter notebook day2.ipynb

# Generate PDF report
jupyter notebook Day3_PDF_Report.ipynb

 About
Built by Gurleen Saini — Data Analyst specialising in business intelligence, predictive analytics, and automated reporting.
Email gurleensainitamber15@gmail.com
 LinkedIn -  | GitHub

Available for freelance data analytics projects. If you need sales analytics, dashboards, or automated reporting for your business — let's talk.
