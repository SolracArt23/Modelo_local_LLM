import os
import sqlite3
import threading


class BD_conn:
    instancia = 0

    def __init__(self):
        BD_conn.instancia = 1
        self.db_path = os.environ.get('DB_PATH', 'db/mi_base.db')
        # ensure directory exists
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        abs_db_path = self.db_path if os.path.isabs(self.db_path) else os.path.join(BASE_DIR, '..', self.db_path)
        os.makedirs(os.path.dirname(abs_db_path), exist_ok=True)

        # connection and lock for thread-safe access
        self._lock = threading.Lock()
        self.db = self.connect(abs_db_path)

    def connect(self, path):
        try:
            # allow connection to be used from different threads
            conn = sqlite3.connect(path, check_same_thread=False)
            return conn
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None

    def execute_query(self, query, params=None):
        if not self.db:
            return None
        try:
            with self._lock:
                cursor = self.db.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.db.commit()
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def Close(self):
        if self.db:
            with self._lock:
                self.db.close()