import os
from flask import Flask
from config import Config
from app.models import init_db
from app.routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    app.config.from_object(config_class)

    # 確保 instance 資料夾存在，以防 SQLite 連線錯誤
    os.makedirs(os.path.dirname(app.config['DATABASE_PATH']), exist_ok=True)

    # 初始化資料庫 (執行 schema.sql)
    init_db()

    # 註冊所有的 Blueprint 路由
    register_blueprints(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
