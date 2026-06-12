import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc#Show all columns when displaying DataFrames.
pd.set_option("display.max_columns", None) import os
os.listdir("Predictive E-Commerce Intelligence Platform")customers = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/olist_customers_dataset.csv"
)

orders = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/olist_orders_dataset.csv"
)

order_items = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/olist_order_items_dataset.csv"
)

payments = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/olist_order_payments_dataset.csv"
)

reviews = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/olist_order_reviews_dataset.csv"
)

products = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/olist_products_dataset.csv"
)

sellers = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/olist_sellers_dataset.csv"
)

category_translation = pd.read_csv(
    "Predictive E-Commerce Intelligence Platform/product_category_name_translation.csv"
)print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)
print("Category Translation:", category_translation.shape)customers.head()customers.info()  customers["customer_id"].nunique()    customers["customer_unique_id"].nunique()     customers["customer_state"].value_counts().head(10)# Customer Table Findings

- Customer table contains 99,441 records.
- No missing values detected.
- customer_id is unique and can be treated as the primary key.
- customer_unique_id contains 96,096 unique values, indicating repeat customers.
- Sao Paulo (SP) has the highest customer concentration with 41,746 customers.orders.info()orders.head()orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])

orders["order_approved_at"] = pd.to_datetime(orders["order_approved_at"])

orders["order_delivered_carrier_date"] = pd.to_datetime(orders["order_delivered_carrier_date"])

orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])

orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"])orders.info()orders["order_status"].value_counts()orders[orders["order_status"] == "canceled"].head()orders["order_id"].nunique()
orders["customer_id"].nunique()## Orders Table Findings

- Orders table contains 99,441 records.
- order_id is unique and serves as the primary key.
- customer_id is unique within the orders table.
- Missing delivery-related dates are associated with non-delivered orders and represent business events rather than data quality issues.
- The Orders table acts as the central transaction table connecting customers, payments, reviews, and order items.order_items.info()order_items.head()order_items["shipping_limit_date"] = pd.to_datetime(order_items["shipping_limit_date"] )order_items.info()order_items["order_id"].nunique()order_items["product_id"].nunique()order_items.groupby("order_id").size().sort_values(ascending = False).head(10)products.info()products.head()products["product_id"].nunique()products.isnull().sum()## Products Table Findings

- Product table contains 32,951 products.
- product_id contains no missing values.
- 610 products (1.85%) have missing category and description-related attributes.
- Only 2 products have missing physical dimensions.
- Overall data quality is high, with missing values concentrated in product metadata.products[products["product_category_name"].isnull()].head()payments.info()payments.head()payments["payment_type"].value_counts()## Payments Table Findings

- Payments table contains 103,886 records.
- No missing values detected.
- Credit cards account for the majority of payments (~74%).
- Installment information is available and can be used for customer spending analysis.
- The number of payment records exceeds the number of orders, indicating that some orders contain multiple payment transactions.payments["order_id"].nunique()payments.groupby("order_id").size().sort_values(ascending=False).head(10)reviews.info()reviews.head()reviews["review_creation_date"] = pd.to_datetime(reviews["review_creation_date"])

reviews["review_answer_timestamp"] = pd.to_datetime(reviews["review_answer_timestamp"])reviews.info()reviews["review_score"].value_counts().sort_index()## Reviews Table Findings

- Reviews table contains 99,224 records.
- Review date columns were converted to datetime.
- Review comments are optional and contain many null values.
- Approximately 77% of reviews are rated 4 or 5 stars.
- 5-star reviews are the most common rating.
- Customer satisfaction appears generally high.sellers.info()sellers.head()sellers["seller_state"].value_counts()## Sellers Table Findings

- Sellers table contains 3,095 sellers.
- Seller distribution is heavily concentrated in São Paulo (SP).
- Approximately 60% of all sellers are located in SP.
- The seller distribution pattern is similar to the customer distribution pattern.category_translation.info()category_translation.head()(customers.isnull().sum())
(orders.isnull().sum())
(order_items.isnull().sum())
(payments.isnull().sum())
(reviews.isnull().sum())
(products.isnull().sum())
(sellers.isnull().sum())print("Customers:", customers.duplicated().sum())
print("Orders:", orders.duplicated().sum())
print("Order Items:", order_items.duplicated().sum())
print("Payments:", payments.duplicated().sum())
print("Reviews:", reviews.duplicated().sum())
print("Products:", products.duplicated().sum())
print("Sellers:", sellers.duplicated().sum())orders.head()orders["delivery_days"] = (orders["order_delivered_customer_date"] - 
                           orders["order_purchase_timestamp"]).dt.days orders["delivery_days"].describe()orders.sort_values(by = "delivery_days", ascending = False) [["order_id", "order_status","delivery_days"]].head(10)orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.daysorders.sort_values(
    by="delivery_days",
    ascending=False
)[[
    "order_id",
    "order_status",
    "delivery_days",
    "delivery_delay_days",
    "order_purchase_timestamp",
    "order_estimated_delivery_date",
    "order_delivered_customer_date"
]].head(10)orders["delivery_delay_days"].describe()orders["order_year"] = orders["order_purchase_timestamp"].dt.year

orders["order_month"] = orders["order_purchase_timestamp"].dt.month

orders["order_day"] = orders["order_purchase_timestamp"].dt.day

orders["order_weekday"] = orders["order_purchase_timestamp"].dt.day_name()orders[[
    "order_purchase_timestamp",
    "order_year",
    "order_month",
    "order_day",
    "order_weekday"
]].head()order_items["total_item_value"] = (
    order_items["price"] +
    order_items["freight_value"]
)#Revenue
order_items[[
    "price",
    "freight_value",
    "total_item_value"
]].head()#shipping percentage
order_items["shipping_pct"] = (
    order_items["freight_value"]
    / order_items["total_item_value"]
) * 100order_items["total_item_value"].describe()order_items.sort_values(
    by="total_item_value",
    ascending=False
)[[
    "order_id",
    "product_id",
    "seller_id",
    "price",
    "freight_value",
    "total_item_value"
]].head(10)## Revenue Feature Findings

- Average item value is 140.64.
- Median item value is 92.32.
- Revenue distribution is positively skewed.
- High-value transactions exist, with the maximum item value reaching 6,929.31
- Outlier investigation is required for premium transactions.order_items["total_item_value"].sum()#Order-Level Revenue
order_revenue = (
    order_items
    .groupby("order_id")["total_item_value"]
    .sum()
    .reset_index()
)

order_revenue.head()order_revenue["total_item_value"].describe()#Average Order Value (AOV)
order_revenue = (
    order_items.groupby("order_id")
    ["total_item_value"].sum().reset_index()
)

order_revenue.head()order_revenue["total_item_value"].describe()#Monthly Revenue Trend

monthly_revenue = (
    order_items.merge(orders[["order_id", "order_purchase_timestamp"]],
                     on = "order_id",
                     how = "left")  
)

monthly_revenue["year_month"] = (
    monthly_revenue["order_purchase_timestamp"].dt.to_period("M")
)

monthly_revenue = (
    monthly_revenue
    .groupby("year_month")["total_item_value"]
    .sum()
    .reset_index()
)

monthly_revenue.head()plt.figure(figsize=(12,6))

plt.plot(
    monthly_revenue["year_month"].astype(str),
    monthly_revenue["total_item_value"],
    color="red"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()#Top Revenue Months
monthly_revenue.sort_values(
    by="total_item_value",
    ascending=False
).head(10)# Monthly Order Trend
monthly_orders = (
    orders.groupby(orders["order_purchase_timestamp"].dt.to_period("M"))
    ["order_id"].count().reset_index()
)

monthly_orders.sort_values(
    by="order_id",
    ascending=False
).head(10)# Creating a new DataFrame
review_delivery_df = orders.merge(
    reviews[["order_id", "review_score"]],
    on="order_id",
    how="inner"
)

review_delivery_df.head()# Checking Correlation
review_delivery_df[
    ["delivery_delay_days", "review_score"]
].corr()# Creating Delay Groups 
review_delivery_df["delivery_group"] = pd.cut(
    review_delivery_df["delivery_delay_days"],
    bins=[-150,-30,-15,-5,0,5,15,200],
    labels = [
        "Very Early",
        "Early",
        "Slightly Early",
        "On Time",
        "Slightly Late",
        "Late",
        "Very Late"
    ]
)#Average Review Score by Delivery Group
review_delivery_analysis = (
    review_delivery_df
    .groupby("delivery_group")["review_score"]
    .mean()
    .reset_index()
)

review_delivery_analysisplt.figure(figsize=(10,5))

plt.bar(
    review_delivery_analysis["delivery_group"],
    review_delivery_analysis["review_score"],
    color="purple"
)

plt.title("Average Review Score by Delivery Performance")
plt.xlabel("Delivery Group")
plt.ylabel("Average Review Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()products_en = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

products_en.head()category_sales = order_items.merge(
    products_en[[
        "product_id",
        "product_category_name_english"
    ]],
    on="product_id",
    how="left"
)

category_sales.head()#Revenue by Category
category_revenue = (
    category_sales
    .groupby("product_category_name_english")["total_item_value"]
    .sum()
    .reset_index()
    .sort_values(
        by="total_item_value",
        ascending=False
    )
)

category_revenue.head(10)#Top Categories by Units Sold
category_units = (
    category_sales
    .groupby("product_category_name_english")
    .size()
    .reset_index(name="units_sold")
    .sort_values(
        by="units_sold",
        ascending=False
    )
)

category_units.head(10)#Average Revenue Per Unit by Category
category_metrics = (
    category_sales
    .groupby("product_category_name_english")
    .agg(
        revenue=("total_item_value", "sum"),
        units_sold=("product_id", "count")
    )
    .reset_index()
)

category_metrics["avg_revenue_per_unit"] = (
    category_metrics["revenue"]
    / category_metrics["units_sold"]
)

category_metrics.sort_values(
    by="avg_revenue_per_unit",
    ascending=False
).head(10)#Seller Revenue Analysis
seller_revenue = (
    order_items
    .groupby("seller_id")
    .agg(
        revenue=("total_item_value", "sum"),
        orders=("order_id", "nunique"),
        products_sold=("product_id", "count")
    )
    .reset_index()
)

seller_revenue.head()#Top Sellers by Revenue
seller_revenue.sort_values(
    by="revenue",
    ascending=False
).head(10)seller_revenue["revenue"].describe()top_10_revenue = (
    seller_revenue
    .sort_values("revenue", ascending=False)
    .head(10)["revenue"]
    .sum()
)

total_revenue = seller_revenue["revenue"].sum()

(top_10_revenue / total_revenue) * 100# State that generates the most orders
customer_orders = orders.merge(
    customers[[
        "customer_id", 
        "customer_state"
    ]],
    on = "customer_id",
    how = "left"
)

state_orders = (
    customer_orders
    .groupby("customer_state")["order_id"]
    .count()
    .reset_index(name="total_orders")
    .sort_values(
        by="total_orders",
        ascending=False
    )
)

state_orders.head(10)# States that generates the most revenue
order_revenue = (
    order_items
    .groupby("order_id")["total_item_value"]
    .sum()
    .reset_index()
)

state_revenue = (
    customer_orders
    .merge(order_revenue, on="order_id")
)

state_revenue_analysis = (
    state_revenue
    .groupby("customer_state")["total_item_value"]
    .sum()
    .reset_index()
    .sort_values(
        by="total_item_value",
        ascending=False
    )
)

state_revenue_analysis.head(10)#Revenue Per Order by State
state_metrics = (
    state_revenue
    .groupby("customer_state")
    .agg(
        revenue=("total_item_value", "sum"),
        orders=("order_id", "nunique")
    )
    .reset_index()
)

state_metrics["revenue_per_order"] = (
    state_metrics["revenue"]
    / state_metrics["orders"]
)

state_metrics.sort_values(
    by="revenue_per_order",
    ascending=False
).head(10)state_orders.head(10)state_revenue_analysis.head(10)state_metrics.sort_values(
    by="revenue_per_order",
    ascending=False
).head(10)#Saving Dashboard Datasets
os.makedirs("data/processed", exist_ok=True)

datasets = {
    "monthly_revenue": monthly_revenue,
    "review_delivery_analysis": review_delivery_analysis,
    "category_revenue": category_revenue,
    "category_units": category_units,
    "category_metrics": category_metrics,
    "seller_revenue": seller_revenue,
    "state_orders": state_orders,
    "state_revenue": state_revenue_analysis,
    "state_metrics": state_metrics
}

for name, df in datasets.items():
    df.to_csv(f"data/processed/{name}.csv", index=False)

print("All datasets saved successfully!")kpi_df = pd.DataFrame({
    "Total Revenue":[order_items["total_item_value"].sum()],
    "Total Orders":[orders["order_id"].nunique()],
    "Total Customers":[customers["customer_unique_id"].nunique()],
    "Average Order Value":[order_revenue["total_item_value"].mean()],
    "Average Delivery Time":[orders["delivery_days"].mean()]
})

kpi_df.to_csv(
    "data/processed/kpi_metrics.csv",
    index=False
)os.listdir("data/processed")!pip install dash plotly
import dash
import plotly

print(dash.__version__)
print(plotly.__version__)def create_card(title, value, subtitle, icon):

    return html.Div(

        [

            html.H4(
                f"{icon} {title}",
                style={
                    "color": "#9CA3AF",
                    "marginBottom": "10px"
                }
            ),

            html.H2(
                value,
                style={
                    "color": "white",
                    "marginBottom": "5px"
                }
            ),

            html.P(
                subtitle,
                style={
                    "color": "#6B7280"
                }
            )

        ],

        style={
            "backgroundColor": "#1F2937",
            "padding": "20px",
            "borderRadius": "15px",
            "width": "18%",
            "textAlign": "center"
        }

    )#Create the 5 Cards
revenue_card = create_card(
    title="Revenue",
    value="15.84M",
    subtitle="Marketplace Revenue",
    icon="💰"
)

orders_card = create_card(
    title="Orders",
    value="99,441",
    subtitle="Total Orders",
    icon="📦"
)

customers_card = create_card(
    title="Customers",
    value="96,096",
    subtitle="Unique Buyers",
    icon="👥"
)

aov_card = create_card(
    title="AOV",
    value="160.58",
    subtitle="Avg Order Value",
    icon="🛒"
)

delivery_card = create_card(
    title="Delivery",
    value="12.09 Days",
    subtitle="Avg Delivery Time",
    icon="🚚"
)#Creating KPI row
kpi_row = html.Div(

    [
        revenue_card,
        orders_card,
        customers_card,
        aov_card,
        delivery_card
    ],

    style={
        "display": "flex",
        "justifyContent": "space-between",
        "marginTop": "40px"
    }

)from dash import Dash, html, dcc
# ==========================
# LOAD DATA
# ==========================

kpi_df = pd.read_csv("data/processed/kpi_metrics.csv")
monthly_revenue = pd.read_csv("data/processed/monthly_revenue.csv")
state_revenue = pd.read_csv("data/processed/state_revenue.csv")

# ==========================
# KPI VALUES
# ==========================

total_revenue = round(kpi_df["Total Revenue"][0], 2)
total_orders = int(kpi_df["Total Orders"][0])
total_customers = int(kpi_df["Total Customers"][0])
aov = round(kpi_df["Average Order Value"][0], 2)
avg_delivery = round(kpi_df["Average Delivery Time"][0], 2)

# ==========================
# KPI CARD FUNCTION
# ==========================

def create_card(title, value, subtitle):

    return html.Div(
        [

            html.H4(
                f"{icon} {title}",
                style={
                    "color": "#9CA3AF"
                }
            ),

            html.H2(
                value,
                style={
                    "color": "white"
                }
            ),

            html.P(
                subtitle,
                style={
                    "color": "#6B7280"
                }
            )

        ],

        style={
            "backgroundColor": "#1F2937",
            "padding": "20px",
            "borderRadius": "15px",
            "width": "18%",
            "textAlign": "center"
        }
    )

# ==========================
# KPI ROW
# ==========================

kpi_row = html.Div(

    [

        create_card(
            "Revenue",
            f"${total_revenue:,.0f}",
            "Marketplace Revenue",
        ),

        create_card(
            "Orders",
            f"{total_orders:,}",
            "Total Orders",
        ),

        create_card(
            "Customers",
            f"{total_customers:,}",
            "Unique Buyers",
        ),

        create_card(
            "AOV",
            f"${aov}",
            "Average Order Value",
        ),

        create_card(
            "Delivery",
            f"{avg_delivery} Days",
            "Average Delivery Time",
        )

    ],

    style={
        "display": "flex",
        "justifyContent": "space-between",
        "marginTop": "40px"
    }
)

# ==========================
# CHARTS
# ==========================

fig_monthly = px.line(
    monthly_revenue,
    x="year_month",
    y="total_item_value",
    title="Monthly Revenue Trend"
)

fig_monthly.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white"
)

fig_state = px.bar(
    state_revenue.head(10),
    x="customer_state",
    y="total_item_value",
    title="Top States by Revenue"
)

fig_state.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white"
)

app = Dash(__name__)

app.layout = html.Div(

    style={
        "backgroundColor": "#111827",
        "minHeight": "100vh",
        "padding": "30px",
        "fontFamily": "Arial"
    },

    children=[

        html.H1(
            "Predictive E-Commerce Intelligence Platform",
            style={
                "color": "white",
                "textAlign": "center"
            }
        ),

        html.P(
            "Interactive dashboard for revenue, customer satisfaction, product performance, seller intelligence, and geographic insights.",
            style={
                "color": "#D1D5DB",
                "textAlign": "center",
                "fontSize": "18px"
            }
        ),

        kpi_row,

        html.Br(),

        dcc.Graph(
            figure=fig_monthly
        ),

        dcc.Graph(
            figure=fig_state
        )

    ]
)

app.run(
    debug=True,
    port=8090
)# Dashboard Insights

The dashboard provides a comprehensive view of marketplace performance and helps answer key business questions:

* How is revenue changing over time?
* Which product categories generate the highest revenue and sales volume?
* Which categories represent premium, high-value purchases?
* How does delivery performance impact customer satisfaction?
* Which sellers contribute the most revenue to the marketplace?
* Which states generate the highest orders and revenue?
* Which regions have the highest customer spending per order?

The dashboard transforms raw e-commerce data into actionable insights, enabling data-driven decisions across sales, operations, customer experience, and marketplace growth.
#Customer Satisfaction vs Delivery Performance
fig = px.bar(
    review_delivery_analysis,
    x = "delivery_group",
    y = "review_score",
    color = "review_score",
    text = "review_score",
    title = "Impact of Delivery Performance on Customer Satisfaction",
    color_continuous_scale = "RdYlGn"
)

fig.update_traces(
    texttemplate = "%{text:0.2f}",
    textposition = "outside"
)

fig.update_layout(
    title_x = 0.5,
    xaxis_title = "Delivery Performance",
    yaxis_title = "Average Review Score",
    height = 600,
    coloraxis_showscale = False
)
fig.show()## Key Findings

- Customers receiving orders early or on time provide ratings above 4 stars.
- Slightly late deliveries reduce ratings to approximately 3 stars.
- Late and very late deliveries result in ratings below 2 stars.
- Delivery performance has a significant impact on customer satisfaction.

## Business Impact

Improving logistics and reducing delivery delays can substantially improve customer experience and review ratings.import plotly.express as px

fig = px.scatter_3d(
    category_metrics,
    x="units_sold",
    y="revenue",
    z="avg_revenue_per_unit",
    color="revenue",
    size="avg_revenue_per_unit",
    hover_name="product_category_name_english",
    title="Category Intelligence Matrix",
    color_continuous_scale="Turbo"
)

fig.update_layout(
    title_x=0.5,
    height=750,

    paper_bgcolor="#111827",
    font_color="white",

    scene=dict(
        xaxis_title="Units Sold",
        yaxis_title="Revenue",
        zaxis_title="Average Revenue Per Unit",

        bgcolor="#1F2937",

        xaxis=dict(
            backgroundcolor="#1F2937",
            gridcolor="gray",
            color="white"
        ),

        yaxis=dict(
            backgroundcolor="#1F2937",
            gridcolor="gray",
            color="white"
        ),

        zaxis=dict(
            backgroundcolor="#1F2937",
            gridcolor="gray",
            color="white"
        )
    )
)

fig.show()## Key Findings

- A small number of categories generate the majority of marketplace revenue.
- Several premium categories achieve high revenue per unit despite lower sales volume.
- High-volume categories form the core revenue drivers of the marketplace.
- Many categories belong to the long-tail segment with relatively low contribution.

## Business Impact

The marketplace should continue investing in top-performing categories while developing targeted strategies for premium niche categories.top_categories = category_metrics.nlargest(
    10,
    "revenue"
)#Premium Category Analysis
fig = px.scatter(
    top_categories,
    x="units_sold",
    y="revenue",
    size="avg_revenue_per_unit",
    color="revenue",
    hover_name="product_category_name_english",
    title="Premium Category Analysis",
    color_continuous_scale="Turbo"
)

fig.update_layout(
    title_x=0.5,
    height=700,
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
    font_color="white"
)

fig.update_xaxes(
    title="Units Sold",
    gridcolor="gray"
)

fig.update_yaxes(
    title="Revenue",
    gridcolor="gray"
)

fig.update_traces(
    textposition = "top center"
)
fig.show()## Key Findings

- Revenue is not driven solely by sales volume.
- Some categories generate significantly higher revenue per unit than others.
- Premium categories can contribute substantial revenue despite lower transaction volumes.
- High-volume categories and premium categories represent different growth opportunities.

## Business Impact

Pricing and category strategy should be customized based on category positioning rather than relying only on sales volume.seller_revenue.head()# Seller Performance
fig = px.scatter_3d(
    seller_revenue,
    x="orders",
    y="revenue",
    z="products_sold",
    color="revenue",
    size="revenue",
    hover_name="seller_id",
    title="Seller Performance Universe",
    color_continuous_scale="Turbo"
)

fig.update_layout(
    title_x=0.5,
    height=750,

    paper_bgcolor="#111827",
    font_color="white",

    scene=dict(
        xaxis_title="Orders",
        yaxis_title="Revenue",
        zaxis_title="Products Sold",

        bgcolor="#1F2937",

        xaxis=dict(
            backgroundcolor="#1F2937",
            gridcolor="gray",
            color="white"
        ),

        yaxis=dict(
            backgroundcolor="#1F2937",
            gridcolor="gray",
            color="white"
        ),

        zaxis=dict(
            backgroundcolor="#1F2937",
            gridcolor="gray",
            color="white"
        )
    )
)

fig.show()## Key Findings

- Seller performance follows a highly concentrated distribution, with a small group of sellers generating a substantial portion of marketplace revenue.
- Most sellers belong to the long-tail segment, contributing relatively low revenue and order volume.
- A strong positive relationship exists between orders, products sold, and revenue generation.
- Several sellers appear to operate in premium segments, generating higher revenue despite comparatively lower order volumes.

## Business Impact

- Marketplace growth is highly dependent on retaining top-performing sellers.
- Long-tail sellers represent an opportunity for seller development and performance improvement programs.
- Premium sellers should be identified and supported through targeted incentives and partnership strategies.
- Seller segmentation can help optimize marketplace growth and resource allocation.#Revenue by State 
fig = px.bar(
    state_revenue.head(10),
    x="customer_state",
    y="total_item_value",
    color="total_item_value",
    text="total_item_value",
    title="Top 10 States by Revenue",
    color_continuous_scale="Turbo"
)

fig.update_traces(
    texttemplate="%{text:.0f}",
    textposition="outside"
)

fig.update_layout(
    title_x=0.5,
    height=650,
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
    font_color="white",
    coloraxis_showscale=False
)

fig.update_xaxes(gridcolor="gray")
fig.update_yaxes(gridcolor="gray")

fig.show()## Key Findings

### Revenue Distribution

- São Paulo (SP) is the dominant market, generating approximately 5.92M in revenue.
- SP generates nearly three times more revenue than the second-ranked state (RJ).
- Revenue is highly concentrated among a small number of states.
- RJ and MG form the second tier of major revenue-generating regions.#Orders by State
fig = px.bar(
    state_orders.head(10),
    x="customer_state",
    y="total_orders",
    color="total_orders",
    text="total_orders",
    title="Top 10 States by Orders",
    color_continuous_scale="Turbo"
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    title_x=0.5,
    height=650,
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
    font_color="white",
    coloraxis_showscale=False
)

fig.show()### Order Volume Analysis

- SP leads with more than 41,000 orders, significantly exceeding all other states.
- The ranking of states by orders closely matches the ranking by revenue.
- This indicates that revenue growth is primarily driven by transaction volume rather than unusually high spending.#Revenue per Order by State
fig = px.bar(
    state_metrics.sort_values(
        "revenue_per_order",
        ascending=False
    ).head(10),
    x="customer_state",
    y="revenue_per_order",
    color="revenue_per_order",
    text="revenue_per_order",
    title="Top States by Revenue Per Order",
    color_continuous_scale="Turbo"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    title_x=0.5,
    height=650,
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
    font_color="white",
    coloraxis_showscale=False
)

fig.show()### Revenue Per Order Analysis

- PB, AC, and AP have the highest revenue per order despite not appearing among the top states by total revenue.
- High revenue per order does not necessarily translate into high overall marketplace revenue.
- Some smaller states exhibit premium purchasing behavior with higher average spending per transaction.

## Business Impact

- São Paulo should remain the primary target for customer acquisition and retention strategies.
- RJ and MG represent important secondary markets with strong revenue potential.
- States with high revenue per order may be suitable targets for premium product campaigns.
- Geographic segmentation can improve marketing efficiency by tailoring strategies to regional purchasing behavior.corr_matrix = review_delivery_df[
    [
        "delivery_days",
        "delivery_delay_days",
        "review_score"
    ]
].corr()

corr_matrixplt.figure(figsize=(8,6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="RdYlGn",
    fmt=".2f"
)

plt.title(
    "Customer Experience Correlation Heatmap"
)

plt.tight_layout()

plt.show()## Key Findings

- Customer review scores decrease as delivery delays increase.
- Delivery time and delivery delay exhibit a positive relationship.
- Delivery performance is one of the strongest drivers of customer satisfaction.
- Customers are highly sensitive to late deliveries.

## Business Impact

- Reducing delivery delays can directly improve customer satisfaction.
- Logistics performance should be treated as a key business metric.
- Investments in fulfillment and delivery optimization may yield significant customer experience improvements.monthly_revenue_clean = monthly_revenue[
    monthly_revenue["total_item_value"] > 10000
].copy()

monthly_revenue_cleanmonthly_revenue_clean["moving_avg_3"] = (
    monthly_revenue_clean["total_item_value"]
    .rolling(3)
    .mean()
)fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=monthly_revenue_clean["year_month"].astype(str),
        y=monthly_revenue_clean["total_item_value"],
        mode="lines+markers",
        name="Monthly Revenue"
    )
)

fig.add_trace(
    go.Scatter(
        x=monthly_revenue_clean["year_month"].astype(str),
        y=monthly_revenue_clean["moving_avg_3"],
        mode="lines",
        name="3-Month Moving Average"
    )
)

fig.update_layout(
    title="Revenue Trend and Moving Average",
    title_x=0.5,
    height=650,
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
    font_color="white"
)

fig.show()## Key Findings

- Marketplace revenue experienced significant growth between 2017 and 2018.
- The 3-month moving average confirms a strong long-term upward trend.
- Revenue growth accelerated during late 2017, indicating rapid marketplace expansion.
- During 2018, revenue stabilized around the 1M mark, suggesting a transition toward a more mature growth stage.

## Business Impact

- The marketplace demonstrated successful customer and seller acquisition during the observation period.
- Sustaining future growth may require expansion into new markets, categories, or customer segments.
- Revenue stability indicates a healthy and established marketplace foundation.monthly_revenue_clean = monthly_revenue_clean.reset_index(drop=True)

monthly_revenue_clean["month_index"] = range(
    len(monthly_revenue_clean)
)#Train Linear Regression Model
from sklearn.linear_model import LinearRegression

X = monthly_revenue_clean[["month_index"]]
y = monthly_revenue_clean["total_item_value"]

model = LinearRegression()

model.fit(X, y)

monthly_revenue_clean["predicted_revenue"] = model.predict(X)from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

y_pred = model.predict(X)

print("R2 Score:", r2_score(y, y_pred))
print("MAE:", mean_absolute_error(y, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y, y_pred)))
print("RMSE:", np.sqrt(mean_squared_error(y, y_pred)))future_months = pd.DataFrame(
    {
        "month_index": range(
            len(monthly_revenue_clean),
            len(monthly_revenue_clean) + 6
        )
    }
)

future_months["forecast_revenue"] = (
    model.predict(future_months)
)

future_monthsfig = go.Figure()

# Actual Revenue
fig.add_trace(
    go.Scatter(
        x=monthly_revenue_clean["year_month"].astype(str),
        y=monthly_revenue_clean["total_item_value"],
        mode="lines+markers",
        name="Actual Revenue"
    )
)

# Regression Trend
fig.add_trace(
    go.Scatter(
        x=monthly_revenue_clean["year_month"].astype(str),
        y=monthly_revenue_clean["predicted_revenue"],
        mode="lines",
        name="Regression Trend"
    )
)

fig.update_layout(
    title="Revenue Trend Forecast Using Linear Regression",
    title_x=0.5,
    height=650,
    paper_bgcolor="#111827",
    plot_bgcolor="#1F2937",
    font_color="white"
)

fig.show()## Key Findings

- Linear Regression indicates a positive long-term revenue trend.
- Forecasted revenue continues to grow over future periods.
- Historical growth patterns suggest sustained marketplace expansion.
- The predictive model estimates continued revenue growth beyond the observed period.

## Business Impact

- Future revenue is expected to remain strong based on historical trends.
- Growth initiatives should continue to capitalize on the positive trajectory.
- Revenue forecasting can support strategic planning, budgeting, and resource allocation.future_months## Predictive Analytics Findings

### Revenue Forecast

- A Linear Regression model was trained using monthly revenue data.
- The model identified a positive long-term relationship between time and revenue.
- Forecasted revenue is expected to increase from approximately 1.33M to 1.59M over the next six periods.
- The projected trend indicates continued marketplace growth.

### Business Impact

- Revenue growth is expected to remain positive if historical trends continue.
- Forecasting can support budgeting, capacity planning, and strategic decision-making.
- Continued investment in customer acquisition and seller expansion may further accelerate growth.
- Future models can be enhanced with seasonality and promotional factors for improved accuracy.