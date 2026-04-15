#导入所要的模块
'''
意思：
Flask：建网站的核心框架
request：接收用户传过来的数据（比如金额、账号）
jsonify：返回中文不乱码的 JSON
CSRFProtect：防伪造请求（黑客不能冒充用户转账）
'''
from flask import Flask, request, jsonify
from flask_wtf.csrf import CSRFProtect

# 补全：跨域、限流、环境变量
from flask_cors import CORS, cross_origin # 跨域白名单
from flask_limiter import Limiter  # 接口限流（防攻击）
from flask_limiter.util import get_remote_address  # 获取访问者IP
from dotenv import load_dotenv # 读取.env密钥
import os  # 读取系统环境

# 加载环境变量
load_dotenv()

# 🔥 解决中文乱码（Flask 3.x 新方案）
app = Flask(__name__)
app.json.ensure_ascii = False
app.json.mimetype = 'application/json;charset=utf-8'

# 从环境变量读取密钥（更安全）
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "test123")  #设置网站加载密钥
app.config['WTF_CSRF_ENABLED'] = True  # 开启CSRF（正式环境必须开）
csrf = CSRFProtect(app) # 初始化CSRF保护 别人不能伪造请求，不能冒充用户转账

# 初始化跨域：只允许信任域名
CORS(app, resources={r"/api/*": {"origins": "http://my-trusted-app.com"}})

# 初始化限流：按IP限制
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day"],  #限制ip每天的访问次数只有200次
)
#对外部展示的数据，只允许信任的域名访问，返回中文不是乱码
@app.route("/api/data")
@cross_origin(origins="http://my-trusted-app.com")
def get_data():
    return jsonify({"msg":"这是安全数据"})

#限制只有post表单访问，接收表单提交的金额
# 返回转账成功提示
# 受CSRF 保护，不能随便伪造
@app.route("/transfer", methods=["POST"])
def transfer():
    amount = request.form.get("amount")
    return f"转账成功：{amount}元"

#防暴力破解密码
@app.route("/login", methods=["POST"])
@limiter.limit("10 per minute")  # 登录接口限流：每分钟10次
def login():
    return "登录接口正常响应"

# 自定义404页面
@app.errorhandler(404)
def page_not_found(error):
    return "页面不存在，请检查地址", 404

# 自定义500服务器错误
@app.errorhandler(500)
def server_error(error):
    return "服务器繁忙，请稍后再试", 500

# 临时测试页面，用来测试 POST
@app.route("/test")
def test():
    return '''
    <form action="/transfer" method="POST">
        金额: <input name="amount" value="100">
        <button type="submit">提交转账</button>
    </form>
    '''
# 启动服务器
if __name__ == '__main__':
    app.run(debug=False)