"""
1. 用户认证
Flask-Security提供了强大的用户认证功能，包括注册、登录、注销等。

通过以下示例代码，快速实现用户认证流程：
"""

# 1. 只导入必需模块（新增login_manager相关）
from flask import Flask, redirect, url_for # 新增：导入login_manager相关
from flask_security import Security, login_required, logout_user # 新增：导入login_manager相关
from flask_login import LoginManager  # 新增：导入LoginManager 

# 2. 定义app实例 + 初始化login_manager（核心修复）
app = Flask(__name__) # 定义app实例
login_manager = LoginManager(app)  # 新增：绑定login_manager到app
login_manager.login_view = 'login'  # 指定登录页路由，必填

# 3. 极简配置（仅保留2个核心，新增login_manager的极简用户加载）
app.config['SECRET_KEY'] = '123456' #设置加密密钥
app.config['SECURITY_PASSWORD_SALT'] = '654321' #密码盐值

# 新增：login_manager必需的用户加载函数（极简模拟，不用数据库）
@login_manager.user_loader # 绑定用户加载函数
def load_user(user_id): # 参数必须是user_id
    # 极简模拟：返回任意有is_authenticated属性的对象即可（满足login_required校验）
    class MockUser: # 定义一个MockUser类
        is_authenticated = True # 设置is_authenticated属性为True
        is_active = True # 设置is_active属性为True
        is_anonymous = False # 设置is_anonymous属性为False
        def get_id(self): # 定义get_id方法
            return user_id # 返回user_id
    return MockUser()

# 4. 初始化Security（新增：绑定app，解决依赖）
security = Security(app)

# 5. 你的原有路由（完全不变）
@app.route('/login') # 新增：登录页路由
def login():
    return "登录页面 <a href='/logout'>测试注销</a>" #一个是文字，一个是链接

@app.route('/logout') # 新增：注销页路由
@login_required  # 现在能正常校验，不报错
def logout(): # 新增：注销函数
    logout_user() # 调用logout_user函数
    return redirect(url_for('login')) # 重定向到登录页

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)