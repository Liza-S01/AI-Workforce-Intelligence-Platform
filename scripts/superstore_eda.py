"""
Superstore Exploratory Data Analysis (EDA) Script.
Calculates all requested business metrics from Sample - Superstore.csv:
1. Category wise profit and loss
2. Most profitable product
3. State and region wise profit
4. Particular date wise sales
5. Month wise sales
6. Difference of order date and ship date (Shipping duration)
7. Segment wise sales
8. Product wise sales
9. City wise sales
10. Product wise discount
11. Most preferable shipping mode
12. Year wise sales
"""
import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPERSTORE_CSV = os.path.join(BASE_DIR, "dataset", "Sample - Superstore.csv")

def run_eda():
    print("=" * 60)
    print("      SUPERSTORE EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 60)
    
    if not os.path.exists(SUPERSTORE_CSV):
        print(f"Error: {SUPERSTORE_CSV} not found!")
        return

    # Handle encoding (usually windows-1252 or latin1)
    try:
        df = pd.read_csv(SUPERSTORE_CSV, encoding="windows-1252")
    except Exception:
        df = pd.read_csv(SUPERSTORE_CSV, encoding="latin1")

    # Clean dates
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M")
    df["ShippingDurationDays"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # 1. Category wise profit and loss
    cat_profit = df.groupby("Category").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Avg_Profit_Margin=("Profit", lambda x: (x.sum() / df.loc[x.index, "Sales"].sum()) * 100)
    ).reset_index()
    print("\n1. Category Wise Sales & Profit:")
    print(cat_profit.to_string(index=False))

    # 2. Most profitable product
    prod_profit = df.groupby("Product Name").agg(
        Total_Profit=("Profit", "sum"),
        Total_Sales=("Sales", "sum")
    ).sort_values(by="Total_Profit", ascending=False).reset_index()
    print(f"\n2. Most Profitable Product:\n   Top 1: {prod_profit.iloc[0]['Product Name']} (Profit: ${prod_profit.iloc[0]['Total_Profit']:,.2f})")

    # 3. State and region wise profit
    state_region_profit = df.groupby(["Region", "State"])["Profit"].sum().reset_index().sort_values(by="Profit", ascending=False)
    print("\n3. Region Wise Total Profit:")
    print(df.groupby("Region")["Profit"].sum().to_string())

    # 4. Particular date wise sales (Sample top 5 dates)
    date_sales = df.groupby("Order Date")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=False)
    print("\n4. Top 5 Sales Dates:")
    print(date_sales.head(5).to_string(index=False))

    # 5. Month wise sales
    month_sales = df.groupby("Month")["Sales"].sum().reset_index()
    print("\n5. Month Wise Sales (Last 6 months sample):")
    print(month_sales.tail(6).to_string(index=False))

    # 6. Difference of order date and ship date
    avg_ship_time = df["ShippingDurationDays"].mean()
    print(f"\n6. Average Shipping Time: {avg_ship_time:.2f} days (Min: {df['ShippingDurationDays'].min()}d, Max: {df['ShippingDurationDays'].max()}d)")

    # 7. Segment wise sales
    segment_sales = df.groupby("Segment").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index()
    print("\n7. Segment Wise Sales:")
    print(segment_sales.to_string(index=False))

    # 8. Product wise sales (Top 5)
    prod_sales = df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).reset_index()
    print("\n8. Top 5 Products by Sales:")
    print(prod_sales.head(5).to_string(index=False))

    # 9. City wise sales (Top 5)
    city_sales = df.groupby("City")["Sales"].sum().sort_values(ascending=False).reset_index()
    print("\n9. Top 5 Cities by Sales:")
    print(city_sales.head(5).to_string(index=False))

    # 10. Product wise discount (Top discounted products)
    prod_discount = df.groupby("Product Name")["Discount"].mean().sort_values(ascending=False).reset_index()
    print("\n10. Top Discounted Products:")
    print(prod_discount.head(5).to_string(index=False))

    # 11. Most preferable shipping mode
    ship_mode = df["Ship Mode"].value_counts().reset_index()
    ship_mode.columns = ["Ship Mode", "Order Count"]
    print("\n11. Most Preferable Shipping Mode:")
    print(ship_mode.to_string(index=False))

    # 12. Year wise sales
    year_sales = df.groupby("Year").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum")
    ).reset_index()
    print("\n12. Year Wise Sales & Profit:")
    print(year_sales.to_string(index=False))
    print("\n" + "=" * 60)

if __name__ == "__main__":
    run_eda()
