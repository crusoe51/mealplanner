import sqlite3
from pathlib import Path

# DOCKER-SICHER: Render ephemeral /tmp/ oder Volume
DB_DIR = Path('/tmp/data') if os.getenv('RENDER') else Path(__file__).parent / "data"
DATABASE_PATH = DB_DIR / "meals.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Einfache Gerichte-Tabelle: nur Name und Farbe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            color TEXT DEFAULT '#3B82F6'
        )
    ''')
    
    # Wochenplan: ein Gericht pro Tag
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meal_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            week INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals(id) ON DELETE CASCADE,
            UNIQUE(year, week, day_of_week)
        )
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_meal_plan_week 
        ON meal_plan(year, week)
    ''')
    
    conn.commit()
    conn.close()
    
    _insert_sample_data()


def _insert_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM meals")
    if cursor.fetchone()[0] == 0:
        sample_meals = [
            ("Spaghetti Bolognese", "#EF4444"),
            ("Hähnchen Curry", "#F59E0B"),
            ("Lachs mit Gemüse", "#3B82F6"),
            ("Pizza", "#EF4444"),
            ("Schnitzel mit Pommes", "#F97316"),
            ("Rinderbraten", "#8B5CF6"),
            ("Gemüse-Quiche", "#14B8A6"),
            ("Lasagne", "#EC4899"),
            ("Fischstäbchen", "#3B82F6"),
            ("Gulasch", "#B91C1C"),
            ("Putengeschnetzeltes", "#F59E0B"),
            ("Reis mit Gemüse", "#22C55E"),
        ]
        
        cursor.executemany(
            'INSERT INTO meals (name, color) VALUES (?, ?)',
            sample_meals
        )
        conn.commit()
    
    conn.close()


# ==================== MEALS ====================

def get_all_meals():
    conn = get_db_connection()
    meals = conn.execute("SELECT * FROM meals ORDER BY name").fetchall()
    conn.close()
    return [dict(meal) for meal in meals]


def get_meal_by_id(meal_id):
    conn = get_db_connection()
    meal = conn.execute("SELECT * FROM meals WHERE id = ?", (meal_id,)).fetchone()
    conn.close()
    return dict(meal) if meal else None


def create_meal(name, color='#3B82F6'):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO meals (name, color) VALUES (?, ?)',
        (name.strip(), color)
    )
    
    meal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return get_meal_by_id(meal_id)


def update_meal(meal_id, name, color):
    conn = get_db_connection()
    conn.execute(
        'UPDATE meals SET name = ?, color = ? WHERE id = ?',
        (name.strip(), color, meal_id)
    )
    conn.commit()
    conn.close()
    return get_meal_by_id(meal_id)


def delete_meal(meal_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
    conn.commit()
    conn.close()
    return True


# ==================== MEAL PLAN ====================

def get_week_plan(year, week):
    conn = get_db_connection()
    
    entries = conn.execute('''
        SELECT mp.day_of_week, m.id, m.name, m.color
        FROM meal_plan mp
        JOIN meals m ON mp.meal_id = m.id
        WHERE mp.year = ? AND mp.week = ?
    ''', (year, week)).fetchall()
    
    conn.close()
    
    # { 0: {id, name, color}, 1: null, 2: {id, name, color}, ... }
    days = {i: None for i in range(7)}
    
    for entry in entries:
        days[entry['day_of_week']] = {
            "id": entry['id'],
            "name": entry['name'],
            "color": entry['color']
        }
    
    return days


def set_day_meal(year, week, day, meal_id):
    conn = get_db_connection()
    conn.execute('''
        INSERT OR REPLACE INTO meal_plan (meal_id, year, week, day_of_week)
        VALUES (?, ?, ?, ?)
    ''', (meal_id, year, week, day))
    conn.commit()
    conn.close()


def clear_day_meal(year, week, day):
    conn = get_db_connection()
    conn.execute('''
        DELETE FROM meal_plan 
        WHERE year = ? AND week = ? AND day_of_week = ?
    ''', (year, week, day))
    conn.commit()
    conn.close()


def clear_week(year, week):
    conn = get_db_connection()
    conn.execute("DELETE FROM meal_plan WHERE year = ? AND week = ?", (year, week))
    conn.commit()
    conn.close()
