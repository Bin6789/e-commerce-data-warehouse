import psycopg2

def extract_and_load():
    source_conn = psycopg2.connect(
        host='staging-db',
        database='staging',
        user='staging_user',
        password='staging_pwd'
    )
    target_conn = psycopg2.connect(
        host='postgres',
        database='dwh',
        user='user',
        password='password'
    )

    src_cur = source_conn.cursor()
    tgt_cur = target_conn.cursor()

    src_cur.execute("SELECT id, name, email FROM users")
    for row in src_cur.fetchall():
        tgt_cur.execute(
            "INSERT INTO dim_user (id, name, email) VALUES (%s, %s, %s) ON CONFLICT (id) DO NOTHING",
            row
        )

    target_conn.commit()
    src_cur.close()
    tgt_cur.close()
    source_conn.close()
    target_conn.close()
