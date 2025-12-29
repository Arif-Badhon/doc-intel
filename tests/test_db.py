import psycopg2

try:
    # Connect as docintel_user
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="docintel_db",
        user="docintel_user",
        password="docintel_pass"
    )
    cur = conn.cursor()
    
    # Test 1: Get version
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    print(f"✅ Connected! PostgreSQL: {version.split()[1]}")
    
    # Test 2: Check tables
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
    tables = cur.fetchall()
    print(f"✅ Tables: {[t[0] for t in tables]}")
    
    # Test 3: Check extensions
    cur.execute("SELECT extname FROM pg_extension ORDER BY extname")
    extensions = cur.fetchall()
    print(f"✅ Extensions: {[e[0] for e in extensions]}")
    
    # Test 4: Insert test data
    cur.execute("INSERT INTO documents (title, content) VALUES (%s, %s) RETURNING id", ("Test", "Test content"))
    doc_id = cur.fetchone()[0]
    conn.commit()
    print(f"✅ Inserted document with ID: {doc_id}")
    
    # Test 5: Verify data
    cur.execute("SELECT COUNT(*) FROM documents")
    count = cur.fetchone()[0]
    print(f"✅ Total documents in DB: {count}")
    
    cur.close()
    conn.close()
    print("\n🎉 All tests passed! Your database is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
