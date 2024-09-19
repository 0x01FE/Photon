import psycopg

DATABASE_NAME = "photon"
HOST = "127.0.0.1"
USER = "student"
PORT = 5432

conn: psycopg.connection = psycopg.connect(f"postgresql://student@localhost/photon")

cur = conn.cursor()

cur.execute("SELECT * FROM players;")

out = cur.fetchall()

print(out)



