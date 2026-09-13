import pandas as pd

import re

kyc = pd.read_csv("track1_kyc_records.csv")

pd.set_option("display.max_columns", None)

print("Shape:", kyc.shape)

print("\nColumns:")
print(kyc.columns.tolist())

print("\nFirst 5 rows:")
print(kyc.head())

print("\nData Types:")
print(kyc.dtypes)

print("\nMissing Values:")
print(kyc.isna().sum())

print("\nComplete Duplicate Rows:")
print(kyc.duplicated().sum())


print("Before removing duplicates:", kyc.shape)

print("Duplicate rows:", kyc.duplicated().sum())

kyc = kyc.drop_duplicates().copy()

print("After removing duplicates:", kyc.shape)

print("Remaining duplicate rows:", kyc.duplicated().sum())



def clean_user_id(x):
    if pd.isna(x):
        return pd.NA

    x = str(x).strip().upper()
    x = re.sub(r"[^A-Z0-9]", "", x)

    # Numeric ID ko USR prefix do
    if x.isdigit():
        x = "USR" + x

    # Exact format: USR + 5 digits
    if re.fullmatch(r"USR\d{5}", x):
        return x

    return pd.NA


kyc["user_id_clean"] = kyc["user_id"].apply(clean_user_id)

print("Missing cleaned user_id:", kyc["user_id_clean"].isna().sum())
print("Invalid user_id:", kyc["user_id_clean"].isna().sum())
print("Duplicate user_id:", kyc["user_id_clean"].duplicated().sum())

print(kyc[["user_id", "user_id_clean"]].head(15))

# Expected format: USR + exactly 5 digits
valid_user_id = kyc["user_id_clean"].str.fullmatch(r"USR\d{5}")

print("Missing user_id:", kyc["user_id_clean"].isna().sum())
print("Invalid user_id:", (~valid_user_id).sum())
print("Valid user_id:", valid_user_id.sum())

# Invalid IDs display karo
print("\nInvalid user IDs:")
print(
    kyc.loc[~valid_user_id, ["user_id", "user_id_clean"]]
    .drop_duplicates()
    .head(20)
)

print("\nUnique ID lengths:")
print(kyc["user_id_clean"].str.len().value_counts())

duplicate_users = kyc[
    kyc["user_id_clean"].duplicated(keep=False)
].sort_values("user_id_clean")

print("Rows belonging to duplicate users:", len(duplicate_users))

print(
    duplicate_users[
        ["user_id", "user_id_clean", "full_name", "pan", "aadhaar", "kyc_status"]
    ].head(20)
)

print(
    kyc.groupby("user_id_clean").size()
    .value_counts()
    .sort_index()
)

kyc["record_duplicate"] = kyc.duplicated(
    subset=[
        "user_id_clean",
        "full_name",
        "pan",
        "aadhaar",
        "date_of_birth",
        "city",
        "state",
        "monthly_income",
        "occupation",
        "signup_timestamp",
        "kyc_status",
        "risk_segment"
    ],
    keep=False
)

print("Exact duplicate records:", kyc["record_duplicate"].sum())


user_record_counts = kyc["user_id_clean"].value_counts()

print("Users with multiple records:")
print(user_record_counts[user_record_counts > 1].head(20))

kyc["full_name_clean"] = (
    kyc["full_name"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

print("Missing names:", kyc["full_name_clean"].isna().sum())

print(
    kyc[["full_name", "full_name_clean"]].head(15)
)



user_summary = (
    kyc.groupby("user_id_clean")
    .agg(
        record_count=("user_id_clean", "size"),
        unique_names=("full_name_clean", "nunique"),
        unique_pan=("pan", "nunique"),
        unique_aadhaar=("aadhaar", "nunique"),
        unique_dob=("date_of_birth", "nunique")
    )
)

conflicting_users = user_summary[
    (user_summary["unique_names"] > 1) |
    (user_summary["unique_pan"] > 1) |
    (user_summary["unique_aadhaar"] > 1) |
    (user_summary["unique_dob"] > 1)
]

print("Users with conflicting information:", len(conflicting_users))
print(conflicting_users.head(20))


duplicate_columns = [
    "user_id_clean",
    "full_name_clean",
    "pan",
    "aadhaar",
    "date_of_birth",
    "city",
    "state",
    "monthly_income",
    "occupation",
    "signup_timestamp",
    "kyc_status",
    "risk_segment"
]

kyc["record_duplicate"] = kyc.duplicated(
    subset=duplicate_columns,
    keep=False
)

print("Exact duplicate records:", kyc["record_duplicate"].sum())

print(
    kyc[
        kyc["user_id_clean"].eq("USR10157")
    ][
        [
            "user_id_clean",
            "full_name_clean",
            "pan",
            "aadhaar",
            "date_of_birth",
            "city",
            "state",
            "monthly_income",
            "occupation",
            "signup_timestamp",
            "kyc_status",
            "risk_segment"
        ]
    ].to_string(index=False)
)


duplicate_columns = [
    "user_id_clean",
    "full_name_clean",
    "pan",
    "aadhaar",
    "date_of_birth",
    "city",
    "state",
    "monthly_income",
    "occupation",
    "signup_timestamp",
    "kyc_status",
    "risk_segment"
]

kyc_check = kyc[duplicate_columns].fillna("<MISSING>")

kyc["record_duplicate"] = kyc_check.duplicated(
    keep=False
)

print("Exact duplicate records:", kyc["record_duplicate"].sum())


import re

def clean_pan(x):
    if pd.isna(x):
        return pd.NA

    x = str(x).strip().upper()
    x = re.sub(r"[^A-Z0-9]", "", x)

    if re.fullmatch(r"[A-Z]{5}\d{4}[A-Z]", x):
        return x

    return pd.NA

kyc["pan_clean"] = kyc["pan"].apply(clean_pan)

print("Missing PAN after cleaning:", kyc["pan_clean"].isna().sum())

print(
    "Invalid PAN:",
    (kyc["pan"].notna() & kyc["pan_clean"].isna()).sum()
)

print(kyc[["pan", "pan_clean"]].head(20))

print("Original missing PAN:", kyc["pan"].isna().sum())

print("Cleaned missing PAN:", kyc["pan_clean"].isna().sum())

print(
    "Invalid non-missing PAN:",
    (kyc["pan"].notna() & kyc["pan_clean"].isna()).sum()
)

print("Valid PAN:", kyc["pan_clean"].notna().sum())


invalid_pan = kyc[
    kyc["pan"].notna() & kyc["pan_clean"].isna()
]

print(
    invalid_pan[["user_id_clean", "pan"]]
    .drop_duplicates()
    .head(20)
)

valid_pan = kyc["pan_clean"].dropna()

print("Unique valid PANs:", valid_pan.nunique())

print(
    "Duplicate valid PAN values:",
    valid_pan.duplicated().sum()
)

duplicate_pan_values = (
    valid_pan[valid_pan.duplicated(keep=False)]
    .drop_duplicates()
)

print("PAN values used by multiple records:", len(duplicate_pan_values))

print(duplicate_pan_values.head(20).to_list())

duplicate_pan_rows = kyc[
    kyc["pan_clean"].isin(duplicate_pan_values)
].sort_values("pan_clean")

print(
    duplicate_pan_rows[
        [
            "pan_clean",
            "user_id_clean",
            "full_name_clean",
            "aadhaar",
            "kyc_status"
        ]
    ].head(30).to_string(index=False)
)


pan_user_counts = (
    duplicate_pan_rows.groupby("pan_clean")["user_id_clean"]
    .nunique()
)

print("PANs linked to multiple users:", (pan_user_counts > 1).sum())
print("PANs repeated within same user only:", (pan_user_counts == 1).sum())


