import oracledb


oracledb.init_oracle_client(lib_dir="./instantclient_21_9")


dsn = "db.freesql.com:1521/23ai_34ui2"


connection = oracledb.connect(
    user="BTHOMAS6012_SCHEMA_MHZNN",
    password="setpassword",
    dsn=dsn
)

print("Successfully connected to Oracle Database")


cursor = connection.cursor()
cursor.execute("SELECT * FROM DUAL")

for row in cursor:
    print(row)

cursor.close()
connection.close()