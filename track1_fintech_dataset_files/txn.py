import pandas as pd
import re

txn = pd.read_csv("track1_upi_transactions.csv")

pd.set_option('display.max_columns', None)

print(txn.shape)
print(txn.columns.tolist())
print(txn.head(10))
'''
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
'''
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











