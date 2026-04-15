# 导入 Flask 和数据库模块
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3,os

# 创建 Flask 应用
app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "一个临时测试用的默认密钥")

# 初始化数据库
# 注意：这里直接拼接 SQL，不安全！
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

# 用户登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 安全数据库操作
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # 安全SQL，只查用户名
        sql = "SELECT * FROM users WHERE username = ?"
        cursor.execute(sql, (username,))
        user = cursor.fetchone()
        conn.close()

        # 安全验证哈希密码
        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Login failed!"
            
    return render_template('login.html')
       
# 主页
@app.route('/home')
def home():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    return redirect(url_for('login'))

# 启动应用
if __name__ == '__main__':
    init_db()
    debug_mode = os.environ.get("FLASK_DEBUG", "False") == "True"
    app.run(debug=debug_mode)