import pandas as pd
import json

import re

txn = pd.read_csv("track1_upi_transactions.csv")
kyc = pd.read_csv("track1_kyc_records.csv")
merchant = pd.read_csv("track1_merchants_master.csv")



with open("track1_chargebacks.json", "r") as f:
    chargebacks = json.load(f)

cb = pd.DataFrame(chargebacks)

print(txn.shape)
print(kyc.shape)
print(merchant.shape)
print(cb.shape)

print("\ntxn: \n")
txn.info()
print("\nkyc: \n")
kyc.info()
print("\nmerchant: \n")
merchant.info()
print("\n cb: \n")
cb.info()


def clean_user_id(x):
    if pd.isna(x):
        return None

    x = str(x).upper()
    x = re.sub(r'[^A-Z0-9]', '', x)

    if x.isdigit():
        x = "USR" + x

    if x.startswith("USR"):
        return x

    return None


txn["user_id"] = txn["user_id"].apply(clean_user_id)
kyc["user_id"] = kyc["user_id"].apply(clean_user_id)
cb["user_id"] = cb["user_id"].apply(clean_user_id)


check = pd.read_csv("track1_upi_transactions_cleaned.csv")

print(check.shape)
print(check.head())
print(check.isna().sum())



kyc_check = pd.read_csv("track1_kyc_records_cleaned.csv")

print("Reloaded KYC shape:", kyc_check.shape)

print("\nColumn names:")
print(kyc_check.columns.tolist())

cleaned_columns = [
    "user_id_clean",
    "full_name_clean",
    "pan_clean",
    "aadhaar_clean",
    "dob_clean",
    "city_clean",
    "state_clean",
    "monthly_income_clean",
    "occupation_clean",
    "signup_timestamp_clean",
    "kyc_status_clean",
    "risk_segment_clean"
]

print("\nDuplicate rows after reload:", kyc_check.duplicated().sum())

print("\nMissing values in cleaned columns:")
print(kyc_check[cleaned_columns].isna().sum())




