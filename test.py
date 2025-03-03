import psycopg2
conn = psycopg2.connect(
    dbname="ave_calculator_db",
    user="postgres",
    password="3071",
    host="localhost",
    port="5432"
)
print("Connection successful!")
conn.close()
