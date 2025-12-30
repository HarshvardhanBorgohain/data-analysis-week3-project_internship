"""
Sales Data Analysis Project
---------------------------
This script loads, cleans, analyzes sales data,
and generates a formatted summary report.

Author: Harshvardhan Borgohain
"""

import pandas as pd


# -------------------------------------------------
# Data Loading
# -------------------------------------------------

def load_data(file_path: str) -> pd.DataFrame:
    """
    Load sales data from a CSV file.

    Args:
        file_path (str): Path to the sales CSV file

    Returns:
        pd.DataFrame: Loaded sales data
    """
    return pd.read_csv(file_path)


# -------------------------------------------------
# Data Cleaning
# -------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset by handling missing values
    and removing duplicates.

    Args:
        df (pd.DataFrame): Raw sales data

    Returns:
        pd.DataFrame: Cleaned sales data
    """
    df = df.drop_duplicates()

    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(include="object").columns

    df[numeric_cols] = df[numeric_cols].fillna(0)
    df[text_cols] = df[text_cols].fillna("Unknown")

    return df


# -------------------------------------------------
# Feature Engineering
# -------------------------------------------------

def calculate_total_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create Total_Sales column if not already present.

    Args:
        df (pd.DataFrame): Cleaned sales data

    Returns:
        pd.DataFrame: Updated DataFrame with Total_Sales
    """
    if "Total_Sales" not in df.columns:
        if {"Quantity", "Price"}.issubset(df.columns):
            df["Total_Sales"] = df["Quantity"] * df["Price"]
    return df


# -------------------------------------------------
# Sales Metrics
# -------------------------------------------------

def calculate_metrics(df: pd.DataFrame) -> dict:
    """
    Calculate key sales metrics.

    Args:
        df (pd.DataFrame): Sales data with Total_Sales

    Returns:
        dict: Dictionary containing computed metrics
    """
    metrics = {
        "total_revenue": df["Total_Sales"].sum(),
        "average_order_value": df["Total_Sales"].mean(),
        "best_selling_product": (
            df.groupby("Product")["Total_Sales"].sum().idxmax()
            if "Product" in df.columns else "N/A"
        ),
        "total_units_sold": (
            df["Quantity"].sum() if "Quantity" in df.columns else 0
        )
    }
    return metrics


# -------------------------------------------------
# Reporting
# -------------------------------------------------

def generate_report(metrics: dict) -> None:
    """
    Print a formatted sales analysis report.

    Args:
        metrics (dict): Calculated sales metrics
    """
    print("\n📊 SALES ANALYSIS REPORT")
    print("=" * 40)
    print(f"💰 Total Revenue: ₹{metrics['total_revenue']:,.2f}")
    print(f"🏆 Best-Selling Product: {metrics['best_selling_product']}")
    print(f"📦 Total Units Sold: {metrics['total_units_sold']}")
    print(f"📈 Average Order Value: ₹{metrics['average_order_value']:,.2f}")
    print("=" * 40)
    print("✅ Analysis completed successfully.\n")


# -------------------------------------------------
# Main Execution
# -------------------------------------------------

def main():
    """
    Main function to execute the sales analysis pipeline.
    """
    file_path = "sales_data.csv"

    df = load_data(file_path)
    df = clean_data(df)
    df = calculate_total_sales(df)

    metrics = calculate_metrics(df)
    generate_report(metrics)


if __name__ == "__main__":
    main()
