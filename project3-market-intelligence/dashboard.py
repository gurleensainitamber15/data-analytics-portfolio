import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Market Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS STYLING
# ─────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #1E3A5F;
        text-align: center;
        padding: 10px 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 10px 15px;
        border-radius: 5px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# LOAD DATA FROM DATABASE
# ─────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    conn = sqlite3.connect('market_intelligence.db')
    df_products = pd.read_sql_query("SELECT * FROM products", conn)
    df_history = pd.read_sql_query("SELECT * FROM price_history", conn)
    df_summary = pd.read_sql_query("SELECT * FROM market_summary", conn)
    conn.close()
    return df_products, df_history, df_summary

df_products, df_history, df_summary = load_data()

# ─────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────
st.sidebar.image("https://via.placeholder.com/300x80/1E3A5F/FFFFFF?text=Market+Intel", 
                  use_container_width=True)
st.sidebar.markdown("## Filters")

# Category filter
all_categories = ['All'] + sorted(df_products['category'].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", all_categories)

# Brand filter
if selected_category == 'All':
    available_brands = ['All'] + sorted(df_products['brand'].unique().tolist())
else:
    available_brands = ['All'] + sorted(
        df_products[df_products['category'] == selected_category]['brand'].unique().tolist()
    )
selected_brand = st.sidebar.selectbox("Select Brand", available_brands)

# Price range filter
min_price = int(df_products['current_price'].min())
max_price = int(df_products['current_price'].max())
price_range = st.sidebar.slider(
    "Price Range (Rs.)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)

# Rating filter
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.0, 0.1)

# Stock status filter
stock_options = ['All'] + df_products['stock_status'].unique().tolist()
selected_stock = st.sidebar.selectbox("Stock Status", stock_options)

# Alert filter
show_alerts_only = st.sidebar.checkbox("Show Alerts Only", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Last Updated:** {datetime.now().strftime('%d %b %Y %H:%M')}")

# ─────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────
df_filtered = df_products.copy()

if selected_category != 'All':
    df_filtered = df_filtered[df_filtered['category'] == selected_category]
if selected_brand != 'All':
    df_filtered = df_filtered[df_filtered['brand'] == selected_brand]

df_filtered = df_filtered[
    (df_filtered['current_price'] >= price_range[0]) &
    (df_filtered['current_price'] <= price_range[1])
]
df_filtered = df_filtered[df_filtered['rating'] >= min_rating]

if selected_stock != 'All':
    df_filtered = df_filtered[df_filtered['stock_status'] == selected_stock]
if show_alerts_only:
    df_filtered = df_filtered[df_filtered['alert'] != 'OK']

# ─────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────
st.markdown('<p class="main-header">Market Intelligence Dashboard</p>',
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">Real-time product pricing, competitor analysis and market trends</p>',
            unsafe_allow_html=True)

# ─────────────────────────────────────────
# TOP KPI METRICS ROW
# ─────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Products",
        value=f"{len(df_filtered):,}",
        delta=f"{len(df_filtered) - len(df_products)} filtered"
    )
with col2:
    st.metric(
        label="Avg Price",
        value=f"Rs.{df_filtered['current_price'].mean():,.0f}",
        delta=f"Rs.{df_filtered['current_price'].mean() - df_products['current_price'].mean():,.0f} vs all"
    )
with col3:
    st.metric(
        label="Avg Rating",
        value=f"{df_filtered['rating'].mean():.1f} ⭐",
        delta=f"{df_filtered['rating'].mean() - df_products['rating'].mean():.2f} vs all"
    )
with col4:
    alerts_count = len(df_filtered[df_filtered['alert'] != 'OK'])
    st.metric(
        label="Active Alerts",
        value=alerts_count,
        delta="Need attention" if alerts_count > 0 else "All clear"
    )
with col5:
    out_of_stock = len(df_filtered[df_filtered['stock_status'] == 'Out of Stock'])
    st.metric(
        label="Out of Stock",
        value=out_of_stock,
        delta=f"{out_of_stock/len(df_filtered)*100:.1f}% of products"
        if len(df_filtered) > 0 else "0%"
    )

st.markdown("---")

# ─────────────────────────────────────────
# ROW 1 - CATEGORY AND PRICE CHARTS
# ─────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Average Price by Category")
    cat_price = df_filtered.groupby('category')['current_price'].mean().reset_index()
    cat_price.columns = ['Category', 'Avg Price']
    cat_price = cat_price.sort_values('Avg Price', ascending=True)
    fig1 = px.bar(cat_price, x='Avg Price', y='Category',
                  orientation='h',
                  color='Avg Price',
                  color_continuous_scale='Blues',
                  text=cat_price['Avg Price'].apply(lambda x: f'Rs.{x:,.0f}'))
    fig1.update_traces(textposition='outside')
    fig1.update_layout(showlegend=False, height=350,
                       coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Price Distribution by Category")
    fig2 = px.box(df_filtered, x='category', y='current_price',
                  color='category',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    fig2.update_layout(showlegend=False, height=350,
                       xaxis_title="Category",
                       yaxis_title="Price (Rs.)")
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────
# ROW 2 - COMPETITOR AND RATING ANALYSIS
# ─────────────────────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Our Price vs Competitor Price")
    fig3 = px.scatter(df_filtered,
                      x='current_price',
                      y='competitor_price',
                      color='category',
                      size='rating',
                      hover_data=['product_name', 'brand'],
                      color_discrete_sequence=px.colors.qualitative.Set1)
    fig3.add_shape(type='line',
                   x0=df_filtered['current_price'].min(),
                   y0=df_filtered['current_price'].min(),
                   x1=df_filtered['current_price'].max(),
                   y1=df_filtered['current_price'].max(),
                   line=dict(color='red', dash='dash', width=2))
    fig3.add_annotation(x=df_filtered['current_price'].max() * 0.8,
                        y=df_filtered['current_price'].max() * 0.9,
                        text="Above line = competitor cheaper",
                        showarrow=False,
                        font=dict(color='red', size=11))
    fig3.update_layout(height=380,
                       xaxis_title="Our Price (Rs.)",
                       yaxis_title="Competitor Price (Rs.)")
    st.plotly_chart(fig3, use_container_width=True)

with col_right2:
    st.subheader("Rating Distribution by Brand")
    top_brands = df_filtered.groupby('brand')['rating'].mean().nlargest(8).index
    df_top_brands = df_filtered[df_filtered['brand'].isin(top_brands)]
    fig4 = px.bar(df_top_brands.groupby('brand')['rating'].mean().reset_index(),
                  x='brand', y='rating',
                  color='rating',
                  color_continuous_scale='RdYlGn',
                  text=df_top_brands.groupby('brand')['rating'].mean().reset_index()['rating'].apply(
                      lambda x: f'{x:.1f}'))
    fig4.update_traces(textposition='outside')
    fig4.update_layout(showlegend=False, height=380,
                       coloraxis_showscale=False,
                       xaxis_title="Brand",
                       yaxis_title="Avg Rating")
    st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────
# ROW 3 - PRICE HISTORY CHART
# ─────────────────────────────────────────
st.subheader("Price History Trends (Last 7 Days)")

history_category = st.selectbox(
    "Select Category for Price History",
    sorted(df_history['category'].unique().tolist())
)

df_hist_filtered = df_history[df_history['category'] == history_category]
hist_trend = df_hist_filtered.groupby('date').agg(
    Avg_Price=('price', 'mean'),
    Avg_Competitor=('competitor_price', 'mean')
).reset_index()

fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=hist_trend['date'],
    y=hist_trend['Avg_Price'],
    name='Our Avg Price',
    line=dict(color='#2196F3', width=3),
    mode='lines+markers'
))
fig5.add_trace(go.Scatter(
    x=hist_trend['date'],
    y=hist_trend['Avg_Competitor'],
    name='Competitor Avg Price',
    line=dict(color='#F44336', width=3, dash='dash'),
    mode='lines+markers'
))
fig5.update_layout(
    height=350,
    xaxis_title="Date",
    yaxis_title="Average Price (Rs.)",
    legend=dict(orientation='h', yanchor='bottom', y=1.02)
)
st.plotly_chart(fig5, use_container_width=True)

# ─────────────────────────────────────────
# ROW 4 - ALERTS AND STOCK STATUS
# ─────────────────────────────────────────
col_alert, col_stock = st.columns(2)

with col_alert:
    st.subheader("Active Market Alerts")
    alerts = df_filtered[df_filtered['alert'] != 'OK'].sort_values(
        'price_vs_competitor', ascending=False)

    if len(alerts) == 0:
        st.success("No active alerts for selected filters!")
    else:
        for _, row in alerts.head(8).iterrows():
            if row['alert'] == 'COMPETITOR CHEAPER':
                st.warning(
                    f"**{row['product_name'][:40]}**  \n"
                    f"Our Price: Rs.{row['current_price']:,.0f} | "
                    f"Competitor: Rs.{row['competitor_price']:,.0f} | "
                    f"Gap: Rs.{row['price_vs_competitor']:,.0f}"
                )
            elif row['alert'] == 'OUT OF STOCK':
                st.error(
                    f"**{row['product_name'][:40]}**  \n"
                    f"OUT OF STOCK - Rs.{row['current_price']:,.0f}"
                )
            else:
                st.info(
                    f"**{row['product_name'][:40]}**  \n"
                    f"LOW STOCK - Rs.{row['current_price']:,.0f}"
                )

with col_stock:
    st.subheader("Stock Status Overview")
    stock_counts = df_filtered['stock_status'].value_counts().reset_index()
    stock_counts.columns = ['Status', 'Count']
    colors_stock = {
        'In Stock': '#4CAF50',
        'Low Stock': '#FF9800',
        'Out of Stock': '#F44336'
    }
    fig6 = px.pie(stock_counts,
                  values='Count',
                  names='Status',
                  color='Status',
                  color_discrete_map=colors_stock,
                  hole=0.4)
    fig6.update_layout(height=350)
    st.plotly_chart(fig6, use_container_width=True)

# ─────────────────────────────────────────
# ROW 5 - PRODUCT DATA TABLE
# ─────────────────────────────────────────
st.markdown("---")
st.subheader("Full Product Intelligence Table")

col_search, col_sort = st.columns([3, 1])
with col_search:
    search_term = st.text_input("Search products by name or brand", "")
with col_sort:
    sort_by = st.selectbox("Sort by",
                            ['current_price', 'rating',
                             'competitiveness_score', 'price_vs_competitor'])

df_table = df_filtered.copy()
if search_term:
    df_table = df_table[
        df_table['product_name'].str.contains(search_term, case=False) |
        df_table['brand'].str.contains(search_term, case=False)
    ]

df_table = df_table.sort_values(sort_by, ascending=False)

display_cols = ['product_name', 'brand', 'category',
                'current_price', 'competitor_price',
                'price_vs_competitor', 'rating',
                'stock_status', 'discount_percent', 'alert']

st.dataframe(
    df_table[display_cols].rename(columns={
        'product_name': 'Product',
        'brand': 'Brand',
        'category': 'Category',
        'current_price': 'Our Price',
        'competitor_price': 'Comp Price',
        'price_vs_competitor': 'Price Gap',
        'rating': 'Rating',
        'stock_status': 'Stock',
        'discount_percent': 'Discount %',
        'alert': 'Alert'
    }),
    height=400,
    use_container_width=True
)

# Download button
csv = df_table[display_cols].to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name=f"market_data_{datetime.now().strftime('%Y%m%d')}.csv",
    mime='text/csv'
)

# ─────────────────────────────────────────
# BUSINESS INTELLIGENCE SUMMARY
# ─────────────────────────────────────────
st.markdown("---")
st.subheader("Business Intelligence Summary")

col_bi1, col_bi2, col_bi3 = st.columns(3)

with col_bi1:
    st.markdown("#### Top 5 Competitive Products")
    top_competitive = df_filtered.nlargest(5, 'competitiveness_score')[
        ['product_name', 'brand', 'competitiveness_score', 'rating']
    ]
    for _, row in top_competitive.iterrows():
        st.markdown(
            f"**{row['product_name'][:35]}**  \n"
            f"Score: {row['competitiveness_score']:.0f}/100 | "
            f"Rating: {row['rating']} ⭐"
        )
        st.markdown("---")

with col_bi2:
    st.markdown("#### Discount Analysis")
    disc_summary = df_filtered.groupby('discount_percent').size().reset_index()
    disc_summary.columns = ['Discount %', 'Products']
    fig_disc = px.bar(disc_summary,
                      x='Discount %',
                      y='Products',
                      color='Products',
                      color_continuous_scale='Viridis')
    fig_disc.update_layout(height=300, coloraxis_showscale=False)
    st.plotly_chart(fig_disc, use_container_width=True)

with col_bi3:
    st.markdown("#### Key Market Insights")
    cheapest_cat = df_filtered.groupby('category')['current_price'].mean().idxmin()
    most_rated = df_filtered.groupby('brand')['rating'].mean().idxmax()
    most_alerts = df_filtered[df_filtered['alert'] != 'OK']['category'].value_counts()
    
    st.info(f"Most Affordable Category: **{cheapest_cat}**")
    st.success(f"Highest Rated Brand: **{most_rated}**")
    
    if len(most_alerts) > 0:
        st.warning(
            f"Most Alerts: **{most_alerts.index[0]}** "
            f"({most_alerts.iloc[0]} alerts)"
        )
    
    competitor_cheaper = len(df_filtered[
        df_filtered['price_vs_competitor'] > 1000])
    if competitor_cheaper > 0:
        st.error(
            f"Products where competitor is Rs.1000+ cheaper: **{competitor_cheaper}**"
        )
    else:
        st.success("No major competitor price gaps found!")
   
# ─────────────────────────────────────────
# FOOTER
# ────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"**Market Intelligence Dashboard** | "
    f"Built with Python & Streamlit | "
    f"Data refreshed: {datetime.now().strftime('%d %b %Y %H:%M')} | "
    f"Total products tracked: {len(df_products):,}"
)