import sqlite3
from app.models import get_db_connection

class Record:
    @staticmethod
    def get_all():
        """取得所有收支記錄（包含關聯的分類與帳戶名稱）。"""
        try:
            conn = get_db_connection()
            query = '''
                SELECT r.*, c.name as category_name, a.name as account_name
                FROM records r
                LEFT JOIN categories c ON r.category_id = c.id
                JOIN accounts a ON r.account_id = a.id
                ORDER BY r.date DESC, r.created_at DESC
            '''
            records = conn.execute(query).fetchall()
            conn.close()
            return [dict(rec) for rec in records]
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 取得單筆記錄。"""
        try:
            conn = get_db_connection()
            record = conn.execute('SELECT * FROM records WHERE id = ?', (record_id,)).fetchone()
            conn.close()
            return dict(record) if record else None
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def create(data):
        """新增一筆收支記錄。data 應包含 amount, date, type, note, category_id, account_id。"""
        try:
            conn = get_db_connection()
            cursor = conn.execute('''
                INSERT INTO records (amount, date, type, note, category_id, account_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data.get('amount'), data.get('date'), data.get('type'), 
                data.get('note'), data.get('category_id'), data.get('account_id')
            ))
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            return record_id
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(record_id, data):
        """更新單筆收支記錄。"""
        try:
            conn = get_db_connection()
            conn.execute('''
                UPDATE records 
                SET amount = ?, date = ?, type = ?, note = ?, category_id = ?, account_id = ?
                WHERE id = ?
            ''', (
                data.get('amount'), data.get('date'), data.get('type'), 
                data.get('note'), data.get('category_id'), data.get('account_id'), record_id
            ))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(record_id):
        """刪除單筆記錄。"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
