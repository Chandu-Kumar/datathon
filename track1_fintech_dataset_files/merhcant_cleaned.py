import pandas as pd

import re

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


#======================================================================Bussiness_type_cleaning===================================================


merchants["business_type_clean"] = (
    merchants["business_type"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.upper()
)

print("Missing business types:",
      merchants["business_type_clean"].isna().sum())

print("\nUnique business types:")
print(merchants["business_type_clean"].unique())

print("\nBusiness type counts:")
print(merchants["business_type_clean"].value_counts())

business_type_mapping = {
    "PRIVATE LIMITED": "PRIVATE_LIMITED",
    "PRIVATE-LIMITED": "PRIVATE_LIMITED",

    "SOLE PROPRIETOR": "SOLE_PROPRIETOR",
    "SOLE-PROPRIETOR": "SOLE_PROPRIETOR"
}

merchants["business_type_clean"] = (
    merchants["business_type_clean"].replace(business_type_mapping)
)

print("Unique business types after standardization:",
      merchants["business_type_clean"].nunique())

print("\nFinal business type counts:")
print(merchants["business_type_clean"].value_counts())

#+++++++++++++++++++++++++++++++++++++++++=================================state&city_cleaning+++++++++++=======================================


merchants["city_clean"] = (
    merchants["city"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

merchants["state_clean"] = (
    merchants["state"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title()
)

print("Missing cleaned cities:",
      merchants["city_clean"].isna().sum())

print("Missing cleaned states:",
      merchants["state_clean"].isna().sum())

print("\nUnique cities:")
print(merchants["city_clean"].unique())

print("\nUnique states:")
print(merchants["state_clean"].unique())


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

merchants["city_clean"] = merchants["city_clean"].replace(city_mapping)

print("Unique cities after standardization:",
      merchants["city_clean"].nunique())

print("\nFinal city counts:")
print(merchants["city_clean"].value_counts())


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

expected_state = merchants["city_clean"].map(city_state_mapping)

city_state_mismatch = merchants[
    expected_state.notna()
    & (merchants["state_clean"] != expected_state)
]

print("City-state mismatches:", len(city_state_mismatch))

print("\nMismatch examples:")
print(
    city_state_mismatch[
        ["city_clean", "state_clean"]
    ].head(10)
)


#==========================================================onboarding_cleaning=======================================


def clean_onboarding_date(x):
    if pd.isna(x):
        return pd.NaT

    x = str(x).strip()

    if x == "":
        return pd.NaT

    # Unix timestamp in seconds
    if x.isdigit() and len(x) == 10:
        try:
            return pd.to_datetime(int(x), unit="s")
        except (ValueError, TypeError, OverflowError):
            return pd.NaT

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d",

        "%m-%d-%Y",
        "%d-%m-%Y",

        "%m/%d/%Y",
        "%d/%m/%Y",

        "%d-%b-%Y",
        "%d/%b/%Y",

        "%m/%d/%Y %I:%M %p",
        "%d/%m/%Y %I:%M %p",

        "%m/%d/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M:%S",
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(x, format=fmt)
        except (ValueError, TypeError):
            continue

    return pd.NaT


merchants["onboarding_date_clean"] = merchants[
    "onboarding_date"
].apply(clean_onboarding_date)

print("Missing onboarding dates after advanced cleaning:",
      merchants["onboarding_date_clean"].isna().sum())

print("\nValid onboarding dates:",
      merchants["onboarding_date_clean"].notna().sum())

print("\nMinimum onboarding date:",
      merchants["onboarding_date_clean"].min())

print("Maximum onboarding date:",
      merchants["onboarding_date_clean"].max())

print("\nSample original vs cleaned dates:")
print(
    merchants[
        ["onboarding_date", "onboarding_date_clean"]
    ].head(15)
)


today = pd.Timestamp.today()

future_onboarding = merchants[
    merchants["onboarding_date_clean"] > today
]

print("Future onboarding dates:", len(future_onboarding))

print("\nFuture date examples:")
print(
    future_onboarding[
        ["merchant_id_clean", "onboarding_date_clean"]
    ].head(10)
)


today = pd.Timestamp.today().normalize()

future_mask = merchants["onboarding_date_clean"] > today

print("Future onboarding dates:", future_mask.sum())

# Future dates ko missing mark karna
merchants.loc[future_mask, "onboarding_date_clean"] = pd.NaT

print(
    "Future dates remaining:",
    (merchants["onboarding_date_clean"] > today).sum()
)

print(
    "Missing onboarding dates after validation:",
    merchants["onboarding_date_clean"].isna().sum()
)


#=======================================================settlement_cleaning===============================================


print("Settlement account data type:",
      merchants["settlement_account"].dtype)

print("\nMissing settlement accounts:",
      merchants["settlement_account"].isna().sum())

print("\nSample settlement account values:")
print(
    merchants["settlement_account"]
    .dropna()
    .astype(str)
    .head(20)
    .tolist()
)

print("\nUnique settlement account values:")
print(
    merchants["settlement_account"]
    .dropna()
    .astype(str)
    .nunique()
)


merchants["settlement_account_clean"] = (
    merchants["settlement_account"]
    .astype("string")
    .str.strip()
    .str.upper()
    .replace("", pd.NA)
)

print("Missing settlement accounts after cleaning:",
      merchants["settlement_account_clean"].isna().sum())

print("\nSample original vs cleaned accounts:")
print(
    merchants[
        ["settlement_account", "settlement_account_clean"]
    ]
    .dropna(subset=["settlement_account"])
    .head(20)
)

print("\nUnique cleaned settlement accounts:",
      merchants["settlement_account_clean"].nunique())




def validate_settlement_account(x):
    if pd.isna(x):
        return "MISSING"

    x = str(x).strip().upper()

    if re.fullmatch(r"\d{10}", x):
        return "NUMERIC_ACCOUNT"

    if re.fullmatch(r"X{4}\d{4}", x):
        return "MASKED_ACCOUNT"

    if re.fullmatch(r"[A-Z]{4}\d{13}", x):
        return "ALPHANUMERIC_ACCOUNT"

    return "OTHER"


merchants["settlement_account_type"] = (
    merchants["settlement_account_clean"]
    .apply(validate_settlement_account)
)

print("Settlement account format counts:")
print(merchants["settlement_account_type"].value_counts())

print("\nOther format examples:")
print(
    merchants.loc[
        merchants["settlement_account_type"] == "OTHER",
        ["settlement_account_clean"]
    ].head(20)
)



#===========================================================merchant_status_cleaning==========================================


print("Missing merchant statuses:",
      merchants["merchant_status"].isna().sum())

print("\nUnique merchant statuses:")
print(merchants["merchant_status"].unique())

print("\nMerchant status counts:")
print(merchants["merchant_status"].value_counts())

merchants["merchant_status_clean"] = (
    merchants["merchant_status"]
    .astype("string")
    .str.strip()
    .str.upper()
)

status_mapping = {
    "ACTIVE": "ACTIVE",
    "A": "ACTIVE",
    "LIVE": "ACTIVE",
    "ENABLED": "ACTIVE",

    "INACTIVE": "INACTIVE",
    "I": "INACTIVE",
    "DISABLED": "INACTIVE",
    "CLOSED": "INACTIVE",

    "SUSPENDED": "SUSPENDED",
    "S": "SUSPENDED",
    "HOLD": "SUSPENDED",
    "BLOCKED": "SUSPENDED"
}

merchants["merchant_status_clean"] = (
    merchants["merchant_status_clean"].replace(status_mapping)
)

print("Unique statuses after standardization:",
      merchants["merchant_status_clean"].nunique())

print("\nFinal merchant status counts:")
print(merchants["merchant_status_clean"].value_counts())

print("\nMissing cleaned statuses:",
      merchants["merchant_status_clean"].isna().sum())




