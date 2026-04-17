import sqlite3
from app.models import get_db_connection

class Account:
    @staticmethod
    def get_all():
        """取得所有帳戶的記錄。"""
        try:
            conn = get_db_connection()
            accounts = conn.execute('SELECT * FROM accounts ORDER BY id').fetchall()
            conn.close()
            return [dict(acc) for acc in accounts]
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(account_id):
        """根據 ID 取得單筆帳戶記錄。"""
        try:
            conn = get_db_connection()
            account = conn.execute('SELECT * FROM accounts WHERE id = ?', (account_id,)).fetchone()
            conn.close()
            return dict(account) if account else None
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def create(data):
        """新增一筆帳戶記錄。參數 data 為字典，必須包含 name, initial_balance。"""
        try:
            conn = get_db_connection()
            cursor = conn.execute(
                'INSERT INTO accounts (name, initial_balance) VALUES (?, ?)', 
                (data.get('name'), data.get('initial_balance', 0.0))
            )
            conn.commit()
            account_id = cursor.lastrowid
            conn.close()
            return account_id
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(account_id, data):
        """更新單筆帳戶記錄。"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE accounts SET name = ?, initial_balance = ? WHERE id = ?', 
                (data.get('name'), data.get('initial_balance', 0.0), account_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(account_id):
        """刪除單筆帳戶記錄。"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM accounts WHERE id = ?', (account_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
