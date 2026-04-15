#导入所需要的模块
from flask import Flask,session,jsonify
from werkzeug.routing import BaseConverter
from datetime import timedelta

#app = Flask(__name__)：创建应用
# secret_key：Session 签名必须要有，必须复杂
app = Flask(__name__)
app.secret_key = "my_very_strong_secret_key_123456"

#写入正则转换器
#作用：让路由支持 <regex("规则"):参数> 这种写法。
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]

#添加正则转换器注册给flask
app.url_map.converters["regex"] = RegexConverter

#配制安全核心 Session 安全（会话攻防核心）
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # 设置会话的有效期为 30 分钟
app.config['SESSION_COOKIE_HTTPONLY'] = True # JS 不能读 Cookie（防 XSS）
app.config['SESSION_COOKIE_SECURE'] = False # 本地没 HTTPS，所以 SECURE=False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # 防 CSRF

#添加全局安全的响应头
@app.after_request # 添加安全响应头
def add_security_headers(response): 
    response.headers['X-Frame-Options'] = 'SAMEORIGIN' # 防止页面被嵌入到其他页面中
    response.headers['X-XSS-Protection'] = '1; mode=block'# 防止 XSS 攻击
    response.headers['X-Content-Type-Options'] = 'nosniff' # 防止 MIME 嗅探
    return response

#：写 5 位数字正则路由
@app.route('/user/<regex("\d{5}"):user_id>') #限制ip为5位数字
def get_user(user_id):
    return jsonify({
        "msg": "合法用户ID",
        "user_id": user_id
    })

# 登录、检查、退出路由
@app.route('/login')
def login():
    session['username'] = "test_user"
    session.permanent = True
    return "登录成功！session 已设置"

@app.route('/check')
def check():
    user = session.get('username', '未登录')
    return f"当前登录用户：{user}"

@app.route('/logout')
def logout():
    session.clear()
    return "已退出登录"

if __name__ == '__main__':
    app.run(debug=True)