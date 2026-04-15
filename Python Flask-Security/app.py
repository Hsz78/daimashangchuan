# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'

db = SQLAlchemy(app)

# 定义用户和角色模型
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='user_roles')

# 设置用户数据存储
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Flask-Security的基本用法涉及到设置安全配置、用户模型、以及各种认证和授权的功能。
#上述是一个最简单的例子，它使用了SQLAlchemy作为数据库，并使用了默认的用户认证和授权模型。
# 在实际应用中，你可能需要根据自己的需求进行定制。
#目前我是看不懂先打出来