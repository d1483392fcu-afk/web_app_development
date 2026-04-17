from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.account import Account

bp = Blueprint('accounts', __name__)

@bp.route('/')
def index():
    """顯示各帳戶及餘額"""
    accounts = Account.get_all()
    return render_template('accounts/index.html', accounts=accounts)

@bp.route('/', methods=['POST'])
def create():
    """接收新增帳戶表單並新增至 DB"""
    name = request.form.get('name')
    initial_balance = request.form.get('initial_balance', 0.0)

    if not name:
        flash('帳戶名稱為必填項目！', 'danger')
        return redirect(url_for('accounts.index'))
    
    try:
        initial_balance = float(initial_balance)
    except ValueError:
        flash('初始餘額必須為數字格式！', 'danger')
        return redirect(url_for('accounts.index'))

    data = {
        'name': name.strip(),
        'initial_balance': initial_balance
    }
    
    account_id = Account.create(data)
    if account_id:
        flash('帳戶新增成功！', 'success')
    else:
        flash('新增失敗，請稍後再試。', 'danger')
        
    return redirect(url_for('accounts.index'))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除帳戶"""
    if Account.delete(id):
        flash('帳戶已成功刪除！', 'success')
    else:
        flash('刪除帳戶失敗，可能已有相關連的收支紀錄。', 'danger')
    return redirect(url_for('accounts.index'))
