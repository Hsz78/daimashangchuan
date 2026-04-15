from flask import Flask #导入Flask模块
from flask_sqlalchemy import SQLAlchemy  #导入SQLAlchemy模块

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:123456@localhost:3306/secure_db?ssl_verify_cert=false'

'''
?ssl_verify_cert=false
启用 SSL 加密，但不校验证书（本地开发最稳、最简单、不报错）
? 后面是连接参数
ssl_ca=ca.pem = 要证书（找不到就报错）
ssl_verify_cert=false = 只加密、不校验（你现在用这个最舒服）
'''

app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 2
app.config['SQLALCHEMY_POOL_RECYCLE'] = 300

"""
POOL_SIZE = 10
数据库最多保持 10 个连接（金库 10 把钥匙）
MAX_OVERFLOW = 2
高峰期最多再额外借 2 把
POOL_RECYCLE = 300
连接空闲 5 分钟自动回收，防止占着不还
"""

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #关闭警告

db = SQLAlchemy(app) #初始化SQLAlchemy对象

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

"""
这是ORM 模型，不用写 SQL
以后查用户全靠它，自动防注入
username 唯一，不能为空
"""


@app.route('/user/<username>')
def get_user(username):
    user = User.query.filter_by(username=username).first()

    if user:
        return f"用户名：{user.username}"
    else:
        return "用户不存在"
    
    '''
   没有拼接任何字符串
filter_by 自动参数化
注入 payload 进来也没用
    '''

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)