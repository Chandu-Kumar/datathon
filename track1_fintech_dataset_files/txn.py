import pandas as pd
import re

txn = pd.read_csv("track1_upi_transactions.csv")

pd.set_option('display.max_columns', None)

print(txn.shape)
print(txn.columns.tolist())
print(txn.head(10))

# Preserve original amount
txn["amount_raw"] = txn["amount"]


# Amount cleaning function
def clean_amount(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    # Remove currency symbols
    value = re.sub(r"[₹$,]", "", value)

    # Remove currency prefixes: Rs, INR
    value = re.sub(r"(?i)^(rs\.?|inr)\s*", "", value)

    # Remove commas and extra spaces
    value = value.replace(",", "").strip()

    try:
        amount = float(value)
    except ValueError:
        return None

    return amount

# Apply cleaning
txn["amount_clean"] = txn["amount_raw"].apply(clean_amount)

# Display result
print(txn[["amount_raw", "amount_clean"]].head(20))

print(txn["amount_clean"].isnull().sum())

print(txn["amount_clean"].describe())

negative_txns = txn[txn["amount_clean"] < 0]

print(negative_txns[["txn_id", "amount_raw", "amount_clean", "status"]])

print("Negative transactions:", len(negative_txns))

print(negative_txns["status"].value_counts())

def amount_issue(value):

    if pd.isna(value):
        return "Missing"

    value = str(value).strip()

    if value == "":
        return "Missing"

    cleaned = re.sub(r"[₹$,]", "", value)
    cleaned = re.sub(r"(?i)^(rs\.?|inr)\s*", "", cleaned)
    cleaned = cleaned.replace(",", "").strip()

    try:
        amount = float(cleaned)
    except ValueError:
        return "Invalid"

    if amount < 0:
        return "Negative"

    return None

txn["amount_issue"] = txn["amount_raw"].apply(amount_issue)

print(txn["amount_issue"].value_counts(dropna=False))

#print(txn.head(20))

print(
    txn.loc[
        txn["amount_raw"].astype("string").str.contains(",", na=False),
        ["amount_raw", "amount_clean"]
    ].head(20)
)

print(
    txn.loc[
        txn["amount_clean"] < 0,
        ["txn_id", "amount_raw", "amount_clean", "status"]
    ].head(20)
)

#                                              +++++++++++++++++++++============timestamp_cleaning==============++++++++++++++++++++++++++

print(txn["timestamp"].head(20).to_string())

print(txn["timestamp"].dtype)




import re
import pandas as pd

def clean_timestamp(value):

    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    if value == "":
        return pd.NaT

    # Unix timestamp
    if re.fullmatch(r"\d{10}", value):
        return pd.to_datetime(
            int(value),
            unit="s",
            errors="coerce"
        )

    # YYYY-MM-DD HH:MM:SS
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", value):
        return pd.to_datetime(
            value,
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce"
        )

    # YYYY/MM/DD
    if re.fullmatch(r"\d{4}/\d{2}/\d{2}", value):
        return pd.to_datetime(
            value,
            format="%Y/%m/%d",
            errors="coerce"
        )

    # MM-DD-YYYY HH:MM:SS AM/PM
    if re.fullmatch(r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2} [AP]M", value):
        return pd.to_datetime(
            value,
            format="%m-%d-%Y %I:%M:%S %p",
            errors="coerce"
        )

    # DD/MM/YYYY HH:MM:SS
    if re.fullmatch(r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}", value):
        return pd.to_datetime(
            value,
            format="%d/%m/%Y %H:%M:%S",
            errors="coerce"
        )

    # DD-MM-YYYY HH:MM:SS
    if re.fullmatch(r"\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}", value):
        return pd.to_datetime(
            value,
            format="%d-%m-%Y %H:%M:%S",
            errors="coerce"
        )

    return pd.NaT

txn["timestamp_clean"] = txn["timestamp"].apply(clean_timestamp)

print("Missing timestamps:", txn["timestamp_clean"].isna().sum())

txn["timestamp_issue"] = txn["timestamp_clean"].isna().map({
    True: "Invalid",
    False: None
})

print(txn["timestamp_issue"].value_counts(dropna=False))


#++++++++++++++++++++++++++++++++++++++++===================txn_id=================+++++++++++++++++++++++++++++++++++++

txn["txn_id_raw"] = txn["txn_id"]

print(txn["txn_id"].head(20).to_string())
print(txn["txn_id"].dtype)


print("Missing txn_id:", txn["txn_id"].isna().sum())
print("Duplicate txn_id:", txn["txn_id"].duplicated().sum())
print(txn["txn_id"].astype(str).str.len().value_counts())


duplicate_ids = txn.loc[
    txn["txn_id"].duplicated(keep=False),
    "txn_id"
]

print("Unique duplicated IDs:", duplicate_ids.nunique())
print(duplicate_ids.value_counts().head(20))

print(
    txn[
        txn["txn_id"].isin(duplicate_ids)
    ][
        [
            "txn_id",
            "timestamp",
            "user_id",
            "merchant_id",
            "amount_clean",
            "status"
        ]
    ].sort_values("txn_id").head(30)
)


print(
    "Complete duplicate rows:",
    txn.duplicated().sum()
)
duplicate_ids = txn.loc[
    txn["txn_id"].duplicated(keep=False),
    "txn_id"
]

print("Unique duplicated IDs:", duplicate_ids.nunique())
print("Duplicate occurrences:", len(duplicate_ids))
print("Complete duplicate rows:", txn.duplicated().sum())


before = len(txn)

txn = txn.drop_duplicates().copy()

after = len(txn)

print("Rows before:", before)
print("Rows after:", after)
print("Rows removed:", before - after)
print("Remaining duplicate txn_id:", txn["txn_id"].duplicated().sum())

import re

txn["txn_id_clean"] = txn["txn_id"].astype("string").str.strip().str.upper()

valid_txn_id = txn["txn_id_clean"].str.fullmatch(r"TXN\d{8}")

print("Invalid txn_id:", (~valid_txn_id).sum())
print(txn.loc[~valid_txn_id, ["txn_id", "txn_id_clean"]].head(20))

print("Missing txn_id:", txn["txn_id_clean"].isna().sum())
print("Duplicate txn_id:", txn["txn_id_clean"].duplicated().sum())
print("Total rows:", len(txn))

#+++++++++++++++++++++++++++++=============================user_id_cleaning++++++++++++++++++++++++++++++++++==============================================

txn["user_id_raw"] = txn["user_id"]

print(txn["user_id"].head(20).to_string())
print("Data type:", txn["user_id"].dtype)

print("Missing user_id:", txn["user_id"].isna().sum())

print(
    "User ID length distribution:",
    txn["user_id"].astype("string").str.len().value_counts()
)

print(
    "Unique users:",
    txn["user_id"].nunique()
)


txn["user_id_clean"] = (
    txn["user_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)


valid_user_id = txn["user_id_clean"].str.fullmatch(r"USR\d{5}")

print("Invalid user_id:", (~valid_user_id).sum())

print(
    txn.loc[
        ~valid_user_id,
        ["user_id", "user_id_clean"]
    ].head(20)
)


print("Missing user_id:", txn["user_id_clean"].isna().sum())
print("Unique users:", txn["user_id_clean"].nunique())

#+++++++++++++++++++++++++++++++++=====================================merchent_id===================+++++++===========+++++++++++++++++++++++


txn["merchant_id_raw"] = txn["merchant_id"]

print(txn["merchant_id"].head(20).to_string())
print("Data type:", txn["merchant_id"].dtype)

print("Missing merchant_id:", txn["merchant_id"].isna().sum())

print(
    "Merchant ID length distribution:",
    txn["merchant_id"].astype("string").str.len().value_counts()
)

print(
    "Unique merchants:",
    txn["merchant_id"].nunique()
)

txn["merchant_id_clean"] = (
    txn["merchant_id"]
    .astype("string")
    .str.strip()
    .str.upper()
)

valid_merchant_id = txn["merchant_id_clean"].str.fullmatch(r"MCH\d{4}")

print("Invalid merchant_id:", (~valid_merchant_id).sum())

print(
    txn.loc[
        ~valid_merchant_id,
        ["merchant_id", "merchant_id_clean"]
    ].head(20)
)


print("Missing merchant_id:", txn["merchant_id_clean"].isna().sum())
print("Unique merchants:", txn["merchant_id_clean"].nunique())

#++++++++++++++++++++++++++++++++==============================utr===============================++++++++++++++++++++++++++++++++++++++++++


txn["utr_raw"] = txn["utr"]

print(txn["utr"].head(20).to_string())
print("Data type:", txn["utr"].dtype)

print("Missing UTR:", txn["utr"].isna().sum())

print(
    "UTR length distribution:",
    txn["utr"].astype("string").str.len().value_counts()
)

print(
    "Unique UTRs:",
    txn["utr"].nunique()
)

txn["utr_clean"] = (
    txn["utr"]
    .astype("string")
    .str.strip()
    .str.upper()
    .str.replace(r"\s+", "", regex=True)
)

valid_utr = txn["utr_clean"].str.fullmatch(r"UTR\d{10}")

print("Missing UTR:", txn["utr_clean"].isna().sum())
print("Invalid UTR:", (~valid_utr & txn["utr_clean"].notna()).sum())

print(
    txn.loc[
        ~valid_utr & txn["utr_clean"].notna(),
        ["utr", "utr_clean"]
    ].head(20)
)

print(
    "Duplicate UTRs:",
    txn["utr_clean"].dropna().duplicated().sum()
)

#++++++++++++++++++++++++++++++++++++++++++++++++====================================merchant cateegory code =================================++++++++++++++++++++++++++++++++++++++++++=======


txn["mcc_raw"] = txn["mcc"]

print(txn["mcc"].head(20).to_string())
print("Data type:", txn["mcc"].dtype)

print("Missing MCC:", txn["mcc"].isna().sum())

print(
    "MCC data type:",
    txn["mcc"].dtype
)

print(
    "Unique MCC values:",
    txn["mcc"].nunique()
)

print(
    txn["mcc"].value_counts(dropna=False).head(20)
)


txn["mcc_clean"] = txn["mcc"].astype("Int64")

print("Missing MCC:", txn["mcc_clean"].isna().sum())

print(
    "MCC values:",
    sorted(txn["mcc_clean"].dropna().unique())
)

print(
    "Invalid MCC:",
    (~txn["mcc_clean"].isin([4131, 5411, 5812, 5912, 7011])
     & txn["mcc_clean"].notna()).sum()
)


print(txn["mcc_clean"].value_counts(dropna=False))




