import psycopg

DATABASE_NAME = "photon"
USERNAME = "student"

CONNECTION_STRING = f"dbname={DATABASE_NAME} username={USERNAME}"

def get_player_by_id(player_id: int):
    with psycopg.connect(CONNECTION_STRING) as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM players WHERE id = ?", player_id)

        return cur.fetchall()

def get_player_by_codename(codename: str):
    with psycopg.connect(CONNECTION_STRING) as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM players WHERE codename = ?", codename)

        return cur.fetchall()

print(get_player_by_codename('John'))



