import pandas as pd

merchants = pd.read_csv("track1_merchants_master.csv")

print("Original merchants shape:", merchants.shape)

print("\nColumns:")
print(merchants.columns.tolist())

print("\nFirst 5 rows:")
print(merchants.head())

print("\nMissing values:")
print(merchants.isna().sum())

print("Complete duplicate rows:", merchants.duplicated().sum())

print("Duplicate merchant IDs:", merchants["merchant_id"].duplicated().sum())

print("\nDuplicate merchant ID examples:")
print(
    merchants[merchants["merchant_id"].duplicated(keep=False)]
    .sort_values("merchant_id")
    .head(10)
)



import re

def clean_merchant_id(x):
    if pd.isna(x):
        return pd.NA

    x = str(x).strip().upper()
    x = re.sub(r"[^A-Z0-9]", "", x)

    if x.isdigit():
        x = "MCH" + x

    if re.fullmatch(r"MCH\d{4}", x):
        return x

    return pd.NA


merchants["merchant_id_clean"] = merchants["merchant_id"].apply(
    clean_merchant_id
)

print("Missing cleaned merchant IDs:",
      merchants["merchant_id_clean"].isna().sum())

print("\nSample original vs cleaned IDs:")
print(
    merchants[["merchant_id", "merchant_id_clean"]]
    .head(15)
)

print(
    "Duplicate cleaned merchant IDs:",
    merchants["merchant_id_clean"].duplicated().sum()
)

print("\nDuplicate cleaned merchant ID examples:")
print(
    merchants[
        merchants["merchant_id_clean"].duplicated(keep=False)
    ]
    .sort_values("merchant_id_clean")
    .head(20)
)

merchant_columns = [
    "merchant_name",
    "mcc",
    "merchant_category",
    "business_type",
    "city",
    "state",
    "onboarding_date",
    "settlement_account",
    "merchant_status",
    "declared_avg_ticket_size"
]

merchant_conflicts = (
    merchants.groupby("merchant_id_clean")[merchant_columns]
    .nunique(dropna=True)
)

conflicting_merchants = merchant_conflicts[
    (merchant_conflicts > 1).any(axis=1)
]

print("Merchant IDs with conflicting records:",
      len(conflicting_merchants))

print("\nConflict examples:")
print(conflicting_merchants.head(10))


before_shape = merchants.shape

merchants = merchants.drop_duplicates().copy()

after_shape = merchants.shape

print("Shape before removing duplicates:", before_shape)
print("Shape after removing duplicates:", after_shape)
print("Complete duplicate rows removed:",
      before_shape[0] - after_shape[0])


#=====================================================merchant_name-cleaning===========================================================

merchants["merchant_name_clean"] = (
    merchants["merchant_name"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

print("Missing cleaned merchant names:",
      merchants["merchant_name_clean"].isna().sum())

print("\nOriginal vs cleaned merchant names:")
print(
    merchants[["merchant_name", "merchant_name_clean"]]
    .head(15)
)


#========================================mcc_cleaning================================================


merchants["mcc_clean"] = pd.to_numeric(
    merchants["mcc"],
    errors="coerce"
)

print("Missing MCC values after cleaning:",
      merchants["mcc_clean"].isna().sum())

print("\nMCC data type:",
      merchants["mcc_clean"].dtype)

print("\nUnique MCC values:")
print(merchants["mcc_clean"].unique()[:20])

print("\nMCC summary:")
print(merchants["mcc_clean"].describe())


invalid_mcc = merchants[
    merchants["mcc_clean"].notna()
    & (
        (merchants["mcc_clean"] < 1000)
        | (merchants["mcc_clean"] > 9999)
        | (merchants["mcc_clean"] % 1 != 0)
    )
]

print("Invalid MCC values:", len(invalid_mcc))

print("\nInvalid MCC examples:")
print(invalid_mcc[["mcc", "mcc_clean"]].head(10))



#================================================================merchant_category-cleaning===============================================

merchants["merchant_category_clean"] = (
    merchants["merchant_category"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.upper()
)

print("Missing merchant categories:",
      merchants["merchant_category_clean"].isna().sum())

print("\nUnique merchant categories:")
print(merchants["merchant_category_clean"].unique())

print("\nCategory counts:")
print(merchants["merchant_category_clean"].value_counts())


category_mapping = {
    "HOTEL": "HOSPITALITY",
    "HOTELS": "HOSPITALITY",
    "HOTEL_LODGING": "HOSPITALITY",

    "APPAREL": "CLOTHING",
    "CLOTHS": "CLOTHING",
    "GARMENTS": "CLOTHING",
    "FASHION": "CLOTHING",

    "TRANSPORT": "TRANSPORTATION",
    "TRANSPRT": "TRANSPORTATION",
    "TRAVEL": "TRANSPORTATION",
    "BUS/TAXI": "TRANSPORTATION",

    "RESTAURANTS": "RESTAURANT",
    "EATING PLACE": "RESTAURANT",
    "FOOD": "RESTAURANT",
    "FOOD_SERVICES": "RESTAURANT",

    "DEPT_STORE": "DEPARTMENT STORE",
    "DEPARTMENT STORES": "DEPARTMENT STORE",

    "GROCERY": "GROCERY",
    "GROCERIES": "GROCERY",
    "GROCERY_STORE": "GROCERY",
    "GROCERY STORES": "GROCERY",
    "KIRANA": "GROCERY",

    "MISC RETAIL": "MISCELLANEOUS RETAIL",
    "RETAIL OTHER": "MISCELLANEOUS RETAIL",
    "MISCELLANEOUS": "MISCELLANEOUS RETAIL",

    "BOOKS": "BOOKS_STATIONERY",
    "BOOK STORE": "BOOKS_STATIONERY",
    "STATIONERY": "BOOKS_STATIONERY",

    "MEDICAL": "MEDICAL",
    "MEDICAL_STORE": "MEDICAL",
    "PHARMACY": "MEDICAL",
    "PHARMACIES": "MEDICAL",
    "CHEMIST": "MEDICAL",

    "TELECOM": "TELECOM",
    "PHONE SERVICE": "TELECOM",
    "MOBILE RECHARGE": "TELECOM"
}

merchants["merchant_category_clean"] = (
    merchants["merchant_category_clean"].replace(category_mapping)
)

print("Unique categories after standardization:",
      merchants["merchant_category_clean"].nunique())

print("\nFinal categories:")
print(merchants["merchant_category_clean"].value_counts())


