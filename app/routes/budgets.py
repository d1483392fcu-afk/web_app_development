from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.budget import Budget
from app.models.category import Category

bp = Blueprint('budgets', __name__)

@bp.route('/')
def index():
    """顯示設定的預算及目前花費進度"""
    budgets = Budget.get_all()
    # 預算主要針對「支出」，所以過濾出 type='expense' 的分類供表單選擇
    categories = Category.get_by_type('expense')
    return render_template('budgets/index.html', budgets=budgets, categories=categories)

@bp.route('/', methods=['POST'])
def create():
    """設定預算並寫回 DB"""
    amount = request.form.get('amount')
    month = request.form.get('month')
    category_id = request.form.get('category_id')

    if not amount or not month:
        flash('預算金額與月份為必填！', 'danger')
        return redirect(url_for('budgets.index'))
        
    try:
        amount = float(amount)
        # 如果有傳入 category_id 且不為空字串，轉 int，否則為 None (代表總預算)
        category_id = int(category_id) if category_id else None
    except ValueError:
        flash('金額格式有誤或分類無效！', 'danger')
        return redirect(url_for('budgets.index'))

    data = {
        'amount': amount,
        'month': month,
        'category_id': category_id
    }

    b_id = Budget.create(data)
    if b_id:
        flash('預算設定成功！', 'success')
    else:
        flash('預算設定失敗。可能是此分類在該月（或當月總預算）已經有設定過了。', 'danger')
        
    return redirect(url_for('budgets.index'))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除預算"""
    if Budget.delete(id):
        flash('預算設定已刪除。', 'success')
    else:
        flash('刪除預算失敗。', 'danger')
    return redirect(url_for('budgets.index'))
