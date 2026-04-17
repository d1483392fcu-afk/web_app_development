from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.category import Category

bp = Blueprint('categories', __name__)

@bp.route('/')
def index():
    """顯示所有分類"""
    categories = Category.get_all()
    return render_template('categories/index.html', categories=categories)

@bp.route('/', methods=['POST'])
def create():
    """新增分類並重導向"""
    name = request.form.get('name')
    cat_type = request.form.get('type')

    if not name or not cat_type:
        flash('分類名稱與收支類型皆為必填！', 'danger')
        return redirect(url_for('categories.index'))
        
    if cat_type not in ['income', 'expense']:
        flash('無效的分類類型，必須為收入(income)或支出(expense)！', 'danger')
        return redirect(url_for('categories.index'))

    data = {
        'name': name.strip(),
        'type': cat_type
    }
    
    cat_id = Category.create(data)
    if cat_id:
        flash('分類新增成功！', 'success')
    else:
        flash('分類新增失敗。', 'danger')
        
    return redirect(url_for('categories.index'))

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    """刪除分類"""
    if Category.delete(id):
        flash('分類已刪除！', 'success')
    else:
        flash('刪除分類失敗，可能有收支紀錄正在標記使用此分類中。', 'danger')
    return redirect(url_for('categories.index'))
