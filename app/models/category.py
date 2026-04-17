import sqlite3
from app.models import get_db_connection

class Category:
    @staticmethod
    def get_all():
        """取得所有分類記錄。"""
        try:
            conn = get_db_connection()
            categories = conn.execute('SELECT * FROM categories ORDER BY type, name').fetchall()
            conn.close()
            return [dict(cat) for cat in categories]
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(category_id):
        """取得單一分類記錄。"""
        try:
            conn = get_db_connection()
            cat = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
            conn.close()
            return dict(cat) if cat else None
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def create(data):
        """新增一筆分類記錄。data 需包含 name, type。"""
        try:
            conn = get_db_connection()
            cursor = conn.execute(
                'INSERT INTO categories (name, type) VALUES (?, ?)', 
                (data.get('name'), data.get('type'))
            )
            conn.commit()
            category_id = cursor.lastrowid
            conn.close()
            return category_id
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(category_id, data):
        """更新分類記錄。"""
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE categories SET name = ?, type = ? WHERE id = ?', 
                (data.get('name'), data.get('type'), category_id)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(category_id):
        """刪除分類記錄。"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
