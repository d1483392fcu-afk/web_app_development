from flask import Blueprint, render_template
from app.models.account import Account
from app.models.record import Record
import datetime

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    """
    首頁總覽
    取得本月總花費、餘額，以及最新收支明細並渲染 index.html
    """
    # 取得本月份字串 (YYYY-MM)
    current_month = datetime.date.today().strftime('%Y-%m')
    all_records = Record.get_all()
    
    # 篩選本月花費與收入
    monthly_expenses = sum(
        float(r['amount']) for r in all_records 
        if r['type'] == 'expense' and str(r['date']).startswith(current_month)
    )
    monthly_income = sum(
        float(r['amount']) for r in all_records 
        if r['type'] == 'income' and str(r['date']).startswith(current_month)
    )
    
    # 計算各帳戶與總管的實際餘額 (初始金額 + 該帳戶歷來收入 - 該帳戶歷來支出)
    accounts = Account.get_all()
    account_balances = {}
    total_balance = 0.0
    
    for acc in accounts:
        acc_id = acc['id']
        balance = float(acc['initial_balance'])
        
        acc_records = [r for r in all_records if r['account_id'] == acc_id]
        balance += sum(float(r['amount']) for r in acc_records if r['type'] == 'income')
        balance -= sum(float(r['amount']) for r in acc_records if r['type'] == 'expense')
        
        account_balances[acc['name']] = balance
        total_balance += balance
        
    # 最新 5 筆紀錄
    recent_records = all_records[:5]
    
    return render_template(
        'dashboard/index.html',
        total_balance=total_balance,
        account_balances=account_balances,
        monthly_expenses=monthly_expenses,
        monthly_income=monthly_income,
        recent_records=recent_records
    )
