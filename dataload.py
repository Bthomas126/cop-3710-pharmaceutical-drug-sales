import oracledb
import pandas as pd

# initialize Oracle client
oracledb.init_oracle_client(lib_dir="./instantclient_21_9")

dsn = "db.freesql.com:1521/23ai_34ui2"

connection = oracledb.connect(
    user="BTHOMAS6012_SCHEMA_MHZNN",
    password="AR6AFFK#8SFERGKWOYFZ9mY9OX0635",
    dsn=dsn
)

cursor = connection.cursor()

# load manufacturer
df = pd.read_csv("data/manufacturer.csv")
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO MANUFACTURER (MFR_ID, NAME, COUNTRY) VALUES (:1, :2, :3)",
        (int(row["MFR_ID"]), row["NAME"], row["COUNTRY"])
    )

# load drug_category
df = pd.read_csv("data/drug_category.csv")
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO DRUG_CATEGORY (DRUG_CODE, DESCRIPTION, MFR_ID) VALUES (:1, :2, :3)",
        (row["DRUG_CODE"], row["DESCRIPTION"], int(row["MFR_ID"]))
    )

# load time_period (FIXED DATE)
df = pd.read_csv("data/time_period.csv")
for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO TIME_PERIOD (DATE_ID, YEAR, MONTH, HOUR, WEEKDAY) VALUES (:1, :2, :3, :4, :5)",
        (
            pd.to_datetime(row["DATE_ID"]).date(),
            int(row["Year"]),
            int(row["Month"]),
            int(row["Hour"]),
            row["WEEKDAY"]
        )
    )

# load sales (FIXED DATE)
df = pd.read_csv("data/sales.csv")

data = [
    (
        row["DRUG_CODE"],
        pd.to_datetime(row["DATE_ID"]).date(),
        float(row["UNITS_SOLD"])
    )
    for _, row in df.iterrows()
]

cursor.executemany(
    "INSERT INTO SALES (DRUG_CODE, DATE_ID, UNITS_SOLD) VALUES (:1, :2, :3)",
    data
)

connection.commit()
cursor.close()
connection.close()

print("Data loaded successfully")