import libsql_client
import os
from dotenv import load_dotenv

load_dotenv()

TURSO_URL   = os.environ.get("TURSO_DATABASE_URL", "").replace("libsql://", "https://")
TURSO_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

def get_db():
    return libsql_client.create_client_sync(
        url=TURSO_URL,
        auth_token=TURSO_TOKEN
    )

def init_db():
    with get_db() as client:
        client.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                name  TEXT NOT NULL UNIQUE,
                color TEXT DEFAULT '#3B82F6'
            )
        ''')
        client.execute('''
            CREATE TABLE IF NOT EXISTS meal_plan (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_id     INTEGER NOT NULL,
                year        INTEGER NOT NULL,
                week        INTEGER NOT NULL,
                day_of_week INTEGER NOT NULL,
                FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE,
                UNIQUE(year, week, day_of_week)
            )
        ''')
        client.execute('''
            CREATE INDEX IF NOT EXISTS idx_meal_plan_week
            ON meal_plan(year, week)
        ''')
    _insert_sample_data()


def _insert_sample_data():
    with get_db() as client:
        result = client.execute("SELECT COUNT(*) FROM meals")
        if result.rows[0][0] == 0:
            sample_meals = [
                ("Spaghetti Bolognese", "#EF4444"),
                ("Hähnchen Curry",      "#F59E0B"),
                ("Lachs mit Gemüse",    "#3B82F6"),
                ("Pizza",               "#EF4444"),
                ("Schnitzel mit Pommes","#F97316"),
                ("Rinderbraten",        "#8B5CF6"),
                ("Gemüse-Quiche",       "#14B8A6"),
                ("Lasagne",             "#EC4899"),
                ("Fischstäbchen",       "#3B82F6"),
                ("Gulasch",             "#B91C1C"),
                ("Putengeschnetzeltes", "#F59E0B"),
                ("Reis mit Gemüse",     "#22C55E"),
            ]
            for name, color in sample_meals:
                client.execute(
                    "INSERT INTO meals (name, color) VALUES (?, ?)",
                    [name, color]
                )


# ==================== MEALS ====================

def get_all_meals():
    with get_db() as client:
        result = client.execute("SELECT * FROM meals ORDER BY name")
        return [
            {"id": r[0], "name": r[1], "color": r[2]}
            for r in result.rows
        ]

def get_meal_by_id(meal_id):
    with get_db() as client:
        result = client.execute(
            "SELECT * FROM meals WHERE id = ?", [meal_id]
        )
        if result.rows:
            r = result.rows[0]
            return {"id": r[0], "name": r[1], "color": r[2]}
        return None

def create_meal(name, color='#3B82F6'):
    with get_db() as client:
        client.execute(
            "INSERT INTO meals (name, color) VALUES (?, ?)",
            [name.strip(), color]
        )
        result = client.execute(
            "SELECT * FROM meals WHERE name = ?", [name.strip()]
        )
        r = result.rows[0]
        return {"id": r[0], "name": r[1], "color": r[2]}

def update_meal(meal_id, name, color):
    with get_db() as client:
        client.execute(
            "UPDATE meals SET name = ?, color = ? WHERE id = ?",
            [name.strip(), color, meal_id]
        )
    return get_meal_by_id(meal_id)

def delete_meal(meal_id):
    with get_db() as client:
        client.execute("DELETE FROM meals WHERE id = ?", [meal_id])
    return True


# ==================== MEAL PLAN ====================

def get_week_plan(year, week):
    with get_db() as client:
        result = client.execute('''
            SELECT mp.day_of_week, m.id, m.name, m.color
            FROM meal_plan mp
            JOIN meals m ON mp.meal_id = m.id
            WHERE mp.year = ? AND mp.week = ?
        ''', [year, week])

        days = {i: None for i in range(7)}
        for r in result.rows:
            days[r[0]] = {"id": r[1], "name": r[2], "color": r[3]}
        return days

def set_day_meal(year, week, day, meal_id):
    with get_db() as client:
        client.execute('''
            INSERT OR REPLACE INTO meal_plan (meal_id, year, week, day_of_week)
            VALUES (?, ?, ?, ?)
        ''', [meal_id, year, week, day])

def clear_day_meal(year, week, day):
    with get_db() as client:
        client.execute('''
            DELETE FROM meal_plan
            WHERE year = ? AND week = ? AND day_of_week = ?
        ''', [year, week, day])

def clear_week(year, week):
    with get_db() as client:
        client.execute(
            "DELETE FROM meal_plan WHERE year = ? AND week = ?",
            [year, week]
        )
