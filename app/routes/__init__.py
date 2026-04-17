from app.routes.dashboard import bp as dashboard_bp
from app.routes.records import bp as records_bp
from app.routes.accounts import bp as accounts_bp
from app.routes.categories import bp as categories_bp
from app.routes.budgets import bp as budgets_bp

def register_blueprints(app):
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(records_bp, url_prefix='/records')
    app.register_blueprint(accounts_bp, url_prefix='/accounts')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(budgets_bp, url_prefix='/budgets')
