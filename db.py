import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="automobile_clean",
        user="postgres",
        password="eien1984freedom"
    )

if __name__ == "__main__":
    try:
        conn = get_connection()
        print("Подключение успешно")

        cur = conn.cursor()

        cur.execute("""
        SELECT model
        FROM automobile.auto
        """)

        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()
        conn.close()

    except Exception as e:
        print(e)