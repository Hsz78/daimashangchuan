'''
通过Flask-Security，可以轻松管理用户角色，实现更灵活的权限控制。
以下示例展示了如何定义和使用用户角色：
'''

# models.py

from flask_security import RoleMixin # 新增：导入RoleMixin 混入类
#RoleMixin  给你的 Role 类「免费」添加一些 Flask-Security 必需的属性 / 方法（比如权限校验相关），不用你自己手写，是 Flask-Security 约定好的规范

class Role(db.Model, RoleMixin): # 新增：继承RoleMixin
    id = db.Column(db.Integer(), primary_key=True) #定义id字段，主键
    name = db.Column(db.String(80), unique=True) #定义name字段，字符串类型，唯一索引

#简单的理解
"""
定义 Role 表的「主键字段」id：
db.Column：声明这是数据库表的一个列。
db.Integer()：列的类型是整数。
primary_key=True：标记这个列是主键（唯一标识每一个角色，比如 id=1 对应「管理员」，id=2 对应「普通用户」）。

定义 Role 表的「角色名称字段」name：
db.String(80)：列的类型是字符串，最大长度 80 个字符。
unique=True：约束这个字段的值必须唯一（比如不能有两个「管理员」角色）。
示例值：'admin'（管理员）、'user'（普通用户）、'editor'（编辑）等。

后续实际使用的场景
给用户「张三」分配 admin 角色，他就能访问管理员页面；
给用户「李四」分配 user 角色，他只能访问普通用户页面；
Flask-Security 会基于这个 Role 表自动做权限校验（比如 @roles_required('admin') 装饰器）。
"""

