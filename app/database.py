import psycopg

DATABASE_NAME = "photon"
USERNAME = "student"

CONNECTION_STRING = f"dbname={DATABASE_NAME} user={USERNAME}"

# Returns an empty list if nothing is found
def get_player_by_id(player_id: int):
    with psycopg.connect(CONNECTION_STRING) as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM players WHERE id = %s", (player_id,))

        data = cur.fetchall()
        if data:
            return data[0]
        
        return None

# Returns an empty list if nothing is found
def get_player_by_codename(codename: str):
    with psycopg.connect(CONNECTION_STRING) as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM players WHERE codename = %s", (codename,))

        data = cur.fetchall()
        if data:
            return data[0]
        
        return None

def add_codename(player_id: int, codename: str):
    with psycopg.connect(CONNECTION_STRING) as conn:
        cur = conn.cursor()

        cur.execute("insert into players (id, codename) values (%s, %s);", (player_id, codename))

        conn.commit()