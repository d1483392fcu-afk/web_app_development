import sqlite3
from app.models import get_db_connection

class Budget:
    @staticmethod
    def get_all():
        """取得所有的預算設定。"""
        try:
            conn = get_db_connection()
            query = '''
                SELECT b.*, c.name as category_name
                FROM budgets b
                LEFT JOIN categories c ON b.category_id = c.id
                ORDER BY b.month DESC, b.created_at DESC
            '''
            budgets = conn.execute(query).fetchall()
            conn.close()
            return [dict(b) for b in budgets]
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(budget_id):
        """根據 ID 取得單一預算。"""
        try:
            conn = get_db_connection()
            b = conn.execute('SELECT * FROM budgets WHERE id = ?', (budget_id,)).fetchone()
            conn.close()
            return dict(b) if b else None
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def create(data):
        """設定單月預算。data 需包含 amount, month, category_id。"""
        try:
            conn = get_db_connection()
            cursor = conn.execute('''
                INSERT INTO budgets (amount, month, category_id)
                VALUES (?, ?, ?)
            ''', (data.get('amount'), data.get('month'), data.get('category_id')))
            conn.commit()
            budget_id = cursor.lastrowid
            conn.close()
            return budget_id
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(budget_id, data):
        """更新預算設定。"""
        try:
            conn = get_db_connection()
            conn.execute('''
                UPDATE budgets SET amount = ?, month = ?, category_id = ?
                WHERE id = ?
            ''', (data.get('amount'), data.get('month'), data.get('category_id'), budget_id))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(budget_id):
        """刪除預算。"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM budgets WHERE id = ?', (budget_id,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
