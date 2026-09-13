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

