import pandas as pd
import numpy as np

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

#++++++++++++++++++++++++++++++++++================aadhar_cleaning========================++++++++++++++++++



def clean_aadhaar(x):
    if pd.isna(x):
        return pd.NA

    x = str(x).strip().upper()

    # Masked Aadhaar ko missing treat karo
    if "X" in x:
        return pd.NA

    # Sirf digits rakho
    x = re.sub(r"[^0-9]", "", x)

    # Aadhaar exactly 12 digits ka hona chahiye
    if re.fullmatch(r"\d{12}", x):
        return x

    return pd.NA


kyc["aadhaar_clean"] = kyc["aadhaar"].apply(clean_aadhaar)

print("Original missing Aadhaar:", kyc["aadhaar"].isna().sum())

print("Cleaned missing Aadhaar:", kyc["aadhaar_clean"].isna().sum())

print(
    "Invalid non-missing Aadhaar:",
    (
        kyc["aadhaar"].notna()
        & kyc["aadhaar_clean"].isna()
    ).sum()
)

print("Valid Aadhaar:", kyc["aadhaar_clean"].notna().sum())

print(
    kyc[["aadhaar", "aadhaar_clean"]].head(20)
)

valid_aadhaar = kyc["aadhaar_clean"].dropna()

print("Unique valid Aadhaar:", valid_aadhaar.nunique())

print(
    "Duplicate Aadhaar occurrences:",
    valid_aadhaar.duplicated().sum()
)

aadhaar_user_counts = (
    kyc.dropna(subset=["aadhaar_clean"])
    .groupby("aadhaar_clean")["user_id_clean"]
    .nunique()
)

print(
    "Aadhaar linked to multiple users:",
    (aadhaar_user_counts > 1).sum()
)

print(
    "Aadhaar repeated within same user:",
    (aadhaar_user_counts == 1).sum()
)


#======================================================dob_cleaning=================================================================



def clean_dob(x):
    if pd.isna(x):
        return pd.NaT

    x = str(x).strip()

    if x == "":
        return pd.NaT

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %I:%M %p",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%d-%b-%Y",
        "%Y/%m/%d",
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(x, format=fmt).date()
        except (ValueError, TypeError):
            continue

    return pd.NaT



kyc["dob_clean"] = kyc["date_of_birth"].apply(clean_dob)

print("Original missing DOB:", kyc["date_of_birth"].isna().sum())

print("Cleaned missing DOB:", kyc["dob_clean"].isna().sum())

print(
    "Invalid non-missing DOB:",
    (
        kyc["date_of_birth"].notna()
        & kyc["dob_clean"].isna()
    ).sum()
)

print(kyc[["date_of_birth", "dob_clean"]].head(20))


today = pd.Timestamp.today().normalize()

dob_series = pd.to_datetime(kyc["dob_clean"], errors="coerce")

future_dob = dob_series > today

print("Future DOB values:", future_dob.sum())

print(
    "Future DOB examples:"
)

print(
    kyc.loc[
        future_dob,
        ["user_id_clean", "date_of_birth", "dob_clean"]
    ].head(20)
)


too_old_dob = dob_series < pd.Timestamp("1900-01-01")

print("DOB before 1900:", too_old_dob.sum())

print(
    kyc.loc[
        too_old_dob,
        ["user_id_clean", "date_of_birth", "dob_clean"]
    ].head(20)
)



today = pd.Timestamp.today().normalize()

dob_series = pd.to_datetime(kyc["dob_clean"], errors="coerce")

age = (
    today.year
    - dob_series.dt.year
    - (
        (today.month < dob_series.dt.month)
        |
        (
            (today.month == dob_series.dt.month)
            & (today.day < dob_series.dt.day)
        )
    )
)

minor_users = age < 18

print("Users below 18 years:", minor_users.sum())

print("\nMinor user examples:")
print(
    kyc.loc[
        minor_users,
        ["user_id_clean", "date_of_birth", "dob_clean"]
    ].head(20)
)


#================================================================city&state_cleaning=============================================================



kyc["city_clean"] = (
    kyc["city"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

kyc["state_clean"] = (
    kyc["state"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

print("Missing city values:", kyc["city_clean"].isna().sum())
print("Missing state values:", kyc["state_clean"].isna().sum())

print("\nCity examples:")
print(kyc[["city", "city_clean"]].head(10))

print("\nState examples:")
print(kyc[["state", "state_clean"]].head(10))

print("Unique cities:", kyc["city_clean"].nunique())
print("Unique states:", kyc["state_clean"].nunique())

print("\nAll unique states:")
print(sorted(kyc["state_clean"].dropna().unique()))

print("\nTop 30 cities:")
print(kyc["city_clean"].value_counts().head(30))


city_mapping = {
    "Bombay": "Mumbai",
    "Mumbay": "Mumbai",

    "Blr": "Bengaluru",
    "Bangalore": "Bengaluru",

    "Poona": "Pune",

    "Calcutta": "Kolkata",

    "Madras": "Chennai",

    "Hyd": "Hyderabad",

    "Lko": "Lucknow",

    "Jalandar": "Jalandhar",

    "Jpr": "Jaipur",

    "Asr": "Amritsar",

    "Ldh": "Ludhiana",

    "New Delhi": "Delhi",
    "Dilli": "Delhi"
}

kyc["city_clean"] = kyc["city_clean"].replace(city_mapping)

print("Unique cities after standardization:", kyc["city_clean"].nunique())

print("\nStandardized city counts:")
print(kyc["city_clean"].value_counts())



city_state_mapping = {
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Bengaluru": "Karnataka",
    "Chennai": "Tamil Nadu",
    "Hyderabad": "Telangana",
    "Jaipur": "Rajasthan",
    "Amritsar": "Punjab",
    "Jalandhar": "Punjab",
    "Ludhiana": "Punjab",
    "Delhi": "Delhi",
    "Lucknow": "Uttar Pradesh",
    "Kolkata": "West Bengal"
}

expected_state = kyc["city_clean"].map(city_state_mapping)

city_state_mismatch = kyc[
    expected_state.notna()
    & (kyc["state_clean"] != expected_state)
]

print("City-state mismatches:", len(city_state_mismatch))

print("\nMismatch examples:")
print(
    city_state_mismatch[
        ["city_clean", "state_clean"]
    ].drop_duplicates().head(20)
)


#============================================================monthly_income_cleaning======================================================


print("Monthly income datatype:", kyc["monthly_income"].dtype)

print("\nMissing income values:", kyc["monthly_income"].isna().sum())

print("\nIncome summary:")
print(kyc["monthly_income"].describe())

print("\nIncome examples:")
print(kyc["monthly_income"].head(20).tolist())




def clean_income(x):
    if pd.isna(x):
        return np.nan

    x = str(x).strip().upper()

    # Missing or unavailable text
    if x in ["", "NOT AVAILABLE", "N/A", "NA", "NULL", "NONE"]:
        return np.nan

    # Remove currency labels and symbols
    x = re.sub(r"₹|INR|RS\.?|,", "", x).strip()

    # Handle values like 27.3K
    if x.endswith("K"):
        try:
            value = float(x[:-1].strip()) * 1000
        except ValueError:
            return np.nan
    else:
        try:
            value = float(x)
        except ValueError:
            return np.nan

    # Income cannot be negative or zero
    if value <= 0:
        return np.nan

    return value


kyc["monthly_income_clean"] = kyc["monthly_income"].apply(clean_income)

print("Original missing income:", kyc["monthly_income"].isna().sum())
print("Cleaned missing income:", kyc["monthly_income_clean"].isna().sum())

print("\nCleaned income datatype:", kyc["monthly_income_clean"].dtype)

print("\nIncome summary:")
print(kyc["monthly_income_clean"].describe())

print("\nIncome examples:")
print(
    kyc[
        ["monthly_income", "monthly_income_clean"]
    ].head(20)
)


income = kyc["monthly_income_clean"]

print("Income below ₹5,000:", (income < 5000).sum())
print("Income above ₹2,00,000:", (income > 200000).sum())

print("\nLow income examples:")
print(
    kyc.loc[
        income < 5000,
        ["user_id_clean", "monthly_income", "monthly_income_clean"]
    ].head(20)
)

print("\nHigh income examples:")
print(
    kyc.loc[
        income > 200000,
        ["user_id_clean", "monthly_income", "monthly_income_clean"]
    ].head(20)
)


