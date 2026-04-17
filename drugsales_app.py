

import oracledb


def get_connection():
    oracledb.init_oracle_client(
        lib_dir="/Users/gabrielagurr/Downloads/instantclient_23_3"
    )


    connection = oracledb.connect(

        user="BTHOMAS6012_SCHEMA_MHZNN",
        password="AR6AFFK#8SFERGKWOYFZ9mY9OX0635",
        host="db.freesql.com",
        port=1521,
        service_name="23ai_34ui2"
    )
    return connection



#print results
def print_results(columns, rows):
    if not rows:
        print("\nNo results found.\n")
        return
    print()
    print(" | ".join(columns))
    print("-" * 60)
    for row in rows:
        print(" | ".join(str(item) for item in row))
    print()

    #feature 1 most popular months for a drug

def most_popular_months(conn):
    drug_code = input("Enter drug code: ").strip()


    query = """
        SELECT tp.MONTH, SUM(s.UNITS_SOLD) AS TOTAL_UNITS_SOLD
        FROM SALES s
        JOIN TIME_PERIOD tp
            ON s.DATE_ID = tp.DATE_ID
        WHERE s.DRUG_CODE = :drug_code
        GROUP BY tp.MONTH
        ORDER BY TOTAL_UNITS_SOLD DESC

           
            """

    cur = conn.cursor()
    cur.execute(query, {"drug_code": drug_code})
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    print_results(columns, rows)
    cur.close()

#Feature 2 show manufacturer country for each drug
def drug_countries(conn):
    query = """
    SELECT dc.DRUG_CODE, m.NAME AS MANUFACTURER_NAME, m.COUNTRY
        FROM DRUG_CATEGORY dc
        JOIN MANUFACTURER m 
            ON dc.MFR_ID = m.MFR_ID 
        ORDER BY dc.DRUG_CODE

"""
        



    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    print_results(columns, rows)
    cur.close()


#feature 3 insert/update sales data

def update_sales(conn):
    drug_code = input("Enter drug code: ").strip()
    date_id = input("Enter date (YYYY-MM-DD: ").strip()
    units_sold = input("Enter units sold: ").strip()

    query = """
     MERGE INTO SALES s
     USING (
        SELECT :drug_code AS drug_code,
                TO_DATE(:date_id, 'YYYY-MM-DD') AS date_id,
                :units_sold AS units_sold
            FROM dual
    ) src
    ON (s.DRUG_CODE = src.drug_code AND s.DATE_ID = src.date_id)
    WHEN MATCHED THEN
        UPDATE SET s.UNITS_SOLD = src.units_sold
    WHEN NOT MATCHED THEN
        INSERT (DRUG_CODE, DATE_ID, UNITS_SOLD)
        VALUES (src.drug_code, src.date_id, src.units_sold)"""

    cur = conn.cursor()
    cur.execute(query, {
        "drug_code": drug_code,
        "date_id": date_id,
        "units_sold": int(units_sold)
    })

    conn.commit()
    print("\n Sales Record inserted/updated successfully.\n")
    cur.close()

#Feature 4: Insert/update time_period table

def update_time_period(conn):
    date_id = input("Enter date (YYYY-MM-DD: ").strip()
    year = input("Enter year: ").strip()
    month = input("Enter month: ").strip()
    weekday = input("Enter weekday: ").strip()
    hour = input("Enter hour: ").strip()

    query = """
        MERGE INTO TIME_PERIOD tp
        USING (
            SELECT TO_DATE(:date_id, 'YYYY-MM-DD') AS date_id,
                    :year AS year,
                    :month AS month,
                    :weekday AS weekday,
                    :hour AS hour
            FROM dual
        ) src
        ON (tp.DATE_ID = src.date_id)
        WHEN MATCHED THEN
            UPDATE SET tp.YEAR = src.year,
                        tp.MONTH = src.month,
                        tp.WEEKDAY = src.weekday,
                        tp.HOUR = src.hour
        WHEN NOT MATCHED THEN
            INSERT (DATE_ID, YEAR, MONTH, WEEKDAY, HOUR)
            VALUES (src.date_id, src.year, src.month, src.weekday, src.hour)"""


    cur = conn.cursor()
    cur.execute(query, {
        "date_id": date_id,
        "year": int(year),
        "month": int(month),
        "weekday": weekday,
         "hour": int(hour)
})
    conn.commit()
    print("\nTime period record inserted/updated successfully.\n")
    cur.close()



#feature 5: long-term trends by year

def yearly_trends(conn):
    drug_code = input("Enter drug code: ").strip()

    query = """
    SElECT tp.YEAR, SUM(s.UNITS_SOLD) AS TOTAL_UNITS_SOLD
    FROM SALES s 
    JOIN TIME_PERIOD tp
        ON s.DATE_ID = tp.DATE_ID
    WHERE s.DRUG_CODE = :drug_code
    GROUP BY tp.YEAR
    ORDER BY tp.YEAR 
"""
    cur = conn.cursor()
    cur.execute(query, {"drug_code": drug_code})
    rows = cur.fetchall()
    columns = [col[0] for col in cur.description]
    print_results(columns, rows)
    cur.close()
#main menu

def main():
    connection = None
    try:
        connection = get_connection()
        print("Connected to pharmaceutical database.\n")

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM DUAL")
            for row in cursor:
                print(row)
        while True:
            print("Pharmaceutical Drug Sales Menu")
            print("1. Show most popular months for a drug")
            print("2. Show Manufacturer country for each drug")
            print("3. Insert/update sales data")
            print("4. Insert/update time-period")
            print("5. Show yearly sales trends for a drug")
            print("6. Exit")

            choice = input("Choose an option 1-6: ").strip()

            if choice == "1":
                most_popular_months(connection)
            elif choice == "2":
                drug_countries(connection)
            elif choice == "3":
                update_sales(connection)
            elif choice == "4":
                update_time_period(connection)
            elif choice == "5":
                yearly_trends(connection)
            elif choice == "6":
                print("Thank you for using Pharmaceutical Database.")
                break
            else:
                print("Invalid choice.")


    except Exception as e:
        print(f"\nError: {e}\n")
    finally:
        if connection is not None:
            connection.close()

if __name__ == '__main__':
    main()



