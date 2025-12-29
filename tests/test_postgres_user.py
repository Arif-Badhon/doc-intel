import psycopg2

try:
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="docintel_db",
        user="postgres",
        password="postgres"
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    print(f"✅ Connected as postgres: {cur.fetchone()[0].split()[1]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
