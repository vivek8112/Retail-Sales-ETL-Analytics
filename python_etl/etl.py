import pandas as pd

# ==========================================
# 1. EXTRACT - Read raw Excel files
# ==========================================

customers = pd.read_excel("../raw/Customers.xlsx")
products = pd.read_excel("../raw/Products.xlsx")
sales = pd.read_excel("../raw/Sales.xlsx")


# ==========================================
# 2. TRANSFORM - Standardize data types
# ==========================================

# Clean Quantity text
sales["Quantity"] = (
    sales["Quantity"]
    .astype(str)
    .str.strip()
    .str.replace('"', '', regex=False)
    .str.replace("'", "", regex=False)
)

# Convert Quantity to numeric
sales["Quantity"] = pd.to_numeric(
    sales["Quantity"],
    errors="coerce"
)

# Convert OrderDate to proper date format
sales["OrderDate"] = pd.to_datetime(
    sales["OrderDate"],
    errors="coerce"
)


# ==========================================
# 3. VALIDATE - Identify bad records
# ==========================================

# Duplicate SalesID
duplicate_mask = sales.duplicated(
    subset="SalesID",
    keep=False
)

# Invalid ProductID
invalid_product_mask = ~sales["ProductID"].isin(
    products["ProductID"]
)

# Invalid Quantity
invalid_quantity_mask = (
    sales["Quantity"].isna() |
    (sales["Quantity"] <= 0)
)

# Invalid Date
invalid_date_mask = sales["OrderDate"].isna()


# ==========================================
# 4. CREATE EXCEPTIONS DATASET
# ==========================================

exception_mask = (
    duplicate_mask |
    invalid_product_mask |
    invalid_quantity_mask |
    invalid_date_mask
)

exceptions = sales[exception_mask].copy()


# Add reason for exception
def get_reason(row):
    reasons = []

    if row["SalesID"] in sales[
        duplicate_mask
    ]["SalesID"].values:
        reasons.append("Duplicate SalesID")

    if row["ProductID"] not in products["ProductID"].values:
        reasons.append("Invalid ProductID")

    if pd.isna(row["Quantity"]) or row["Quantity"] <= 0:
        reasons.append("Invalid Quantity")

    if pd.isna(row["OrderDate"]):
        reasons.append("Invalid OrderDate")

    return ", ".join(reasons)


exceptions["ExceptionReason"] = exceptions.apply(
    get_reason,
    axis=1
)


# ==========================================
# 5. CLEAN SALES DATA
# ==========================================

clean_sales = sales[~exception_mask].copy()

# Convert Quantity to integer
clean_sales["Quantity"] = clean_sales["Quantity"].astype(int)


# ==========================================
# 6. CLEAN CUSTOMERS & PRODUCTS
# ==========================================

clean_customers = customers.copy()
clean_products = products.copy()


# ==========================================
# 7. LOAD - Save processed files
# ==========================================

clean_customers.to_csv(
    "../processed/customers_clean.csv",
    index=False
)

clean_products.to_csv(
    "../processed/products_clean.csv",
    index=False
)

clean_sales.to_csv(
    "../processed/sales_clean.csv",
    index=False
)

exceptions.to_csv(
    "../processed/sales_exceptions.csv",
    index=False
)


# ==========================================
# 8. ETL SUMMARY
# ==========================================

print("================================")
print("       ETL PROCESS COMPLETE")
print("================================")

print("Raw sales rows:", len(sales))
print("Clean sales rows:", len(clean_sales))
print("Exception rows:", len(exceptions))

print("\nException details:")
print(
    exceptions[
        ["SalesID", "ExceptionReason"]
    ]
)

print("\nProcessed files created successfully.")