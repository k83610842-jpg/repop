import psycopg2

DB_CONFIG = {
    "dbname": "snake_game",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT NOW()
                );
            """)
        conn.commit()

def get_or_create_player(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING",
                (username,)
            )
            conn.commit()
            cur.execute("SELECT id FROM players WHERE username = %s", (username,))
            return cur.fetchone()[0]

def save_session(player_id, score, level):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (player_id, score, level)
            )
        conn.commit()

def get_personal_best(player_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
                (player_id,)
            )
            result = cur.fetchone()[0]
            return result or 0

def get_top10():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON p.id = gs.player_id
                ORDER BY gs.score DESC
                LIMIT 10
            """)
            return cur.fetchall()
