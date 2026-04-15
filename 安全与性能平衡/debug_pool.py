from flask import Flask, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# 数据库配置（改成你自己的）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/test'
app.config['SQLALCHEMY_POOL_SIZE'] = 5
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 10
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800
app.config['SQLALCHEMY_POOL_PRE_PING'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/debug/db-pool')
def pool_status():
    pool = db.engine.pool

    data = {
        "pool_size": 5,
        "max_overflow": 10,
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "状态": "连接池正常运行 ✅"
    }

    # 强制 UTF-8 输出，确保中文不乱码
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        mimetype="application/json; charset=utf-8"
    )

if __name__ == '__main__':
    app.run(debug=True)