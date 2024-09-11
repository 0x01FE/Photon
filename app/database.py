import psycopg2

DATABASE = ""
HOST = "127.0.0.1"
USER = ""
PORT = 5432

conn: psycopg2.connection = psycopg2.connect(database=DATABASE,
                        host=HOST,
                        user=USER,
                        port=PORT)

cur = conn.cursor()



