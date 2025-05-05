import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_name='todo.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def save_setting(self, key, value):
        try:
            self.cursor.execute('''INSERT OR REPLACE INTO settings (key, value)
                                VALUES (?, ?)''', (key, value))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"保存设置失败: {e}")
            return False

    def get_setting(self, key, default=None):
        self.cursor.execute('''SELECT value FROM settings WHERE key = ?''', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default

    def _create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings
                            (key TEXT PRIMARY KEY,
                             value TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             task TEXT NOT NULL,
                             status TEXT DEFAULT '待办',
                             deadline DATETIME,
                             created_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def add_task(self, task, deadline=None):
        try:
            self.cursor.execute('''INSERT INTO tasks (task, deadline)
                                VALUES (?, ?)''', (task, deadline))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"添加任务失败: {e}")
            return False

    def update_status(self, task_id, new_status):
        try:
            self.cursor.execute('''UPDATE tasks SET status = ?
                                WHERE id = ?''', (new_status, task_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"更新状态失败: {e}")
            return False

    def get_all_tasks(self):
        self.cursor.execute('''SELECT id, task, status, deadline
                            FROM tasks ORDER BY created_at DESC''')
        return self.cursor.fetchall()

    def delete_task(self, task_id):
        try:
            self.cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"删除任务失败: {e}")
            return False

    def __del__(self):
        self.conn.close()