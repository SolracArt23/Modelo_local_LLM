import os, sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
db_path = os.path.join(BASE_DIR, 'db', 'mi_base.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('SELECT id,empresa FROM usuarios')
result = cursor.fetchone()
print(result)