from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.record import Record
from app.models.account import Account
from app.models.category import Category

bp = Blueprint('records', __name__)

@bp.route('/')
def index():
    """顯示所有收支或是篩選結果"""
    records = Record.get_all()
    return render_template('records/index.html', records=records)

@bp.route('/new', methods=['GET'])
def new():
    """顯示新增收支表單，傳入帳戶與分類清單"""
    accounts = Account.get_all()
    categories = Category.get_all()
    return render_template('records/form.html', record=None, accounts=accounts, categories=categories)

@bp.route('/', methods=['POST'])
def create():
    """接收表單並寫入 DB，存檔後重導至列表頁"""
    amount = request.form.get('amount')
    date = request.form.get('date')
    record_type = request.form.get('type')
    account_id = request.form.get('account_id')
    category_id = request.form.get('category_id')
    note = request.form.get('note', '')

    if not all([amount, date, record_type, account_id]):
        flash('除了備註與分類外，金額、日期、類型、帳戶皆為必填項目！', 'danger')
        return redirect(url_for('records.new'))

    try:
        amount = float(amount)
        account_id = int(account_id)
        # 如果使用者有選擇分類，則轉為 integer，否則記錄為 None (無分類)
        category_id = int(category_id) if category_id else None
    except ValueError:
        flash('金額格式錯誤或未選擇有效的帳戶/分類！', 'danger')
        return redirect(url_for('records.new'))

    data = {
        'amount': amount,
        'date': date,
        'type': record_type,
        'note': note.strip(),
        'account_id': account_id,
        'category_id': category_id
    }
    
    if Record.create(data):
        flash('收支明細新增成功！', 'success')
    else:
        flash('新增失敗，請檢查資料格式後重試。', 'danger')

    return redirect(url_for('records.index'))

@bp.route('/<int:id>/edit', methods=['GET'])
def edit(id):
    """顯示帶有原資料的表單"""
    record = Record.get_by_id(id)
    if not record:
        flash('找不到該筆收支紀錄。', 'danger')
        return redirect(url_for('records.index'))
        
    accounts = Account.get_all()
    categories = Category.get_all()
    return render_template('records/form.html', record=record, accounts=accounts, categories=categories)

@bp.route('/<int:id>/update', methods=['POST'])
def update(id):
    """接收表單更新收支資料"""
    amount = request.form.get('amount')
    date = request.form.get('date')
    record_type = request.form.get('type')
    account_id = request.form.get('account_id')
    category_id = request.form.get('category_id')
    note = request.form.get('note', '')

    if not all([amount, date, record_type, account_id]):
        flash('除了備註與分類外，金額、日期、類型、帳戶皆為必填項目！', 'danger')
        return redirect(url_for('records.edit', id=id))

    try:
        amount = float(amount)
        account_id = int(account_id)
        category_id = int(category_id) if category_id else None
    except ValueError:
        flash('金額格式錯誤或未選擇有效的帳戶/分類！', 'danger')
        return redirect(url_for('records.edit', id=id))

    data = {
        'amount': amount,
        'date': date,
        'type': record_type,
        'note': note.strip(),
        'account_id': account_id,
        'category_id': category_id
    }
    
    if Record.update(id, data):
        flash('收支紀錄更新成功！', 'success')
    else:
        flash('紀錄更新失敗，請檢查資料格式後重試。', 'danger')

    return redirect(url_for('records.index'))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除單筆收支"""
    if Record.delete(id):
        flash('收支紀錄已刪除。', 'success')
    else:
        flash('刪除紀錄失敗。', 'danger')
    return redirect(url_for('records.index'))
