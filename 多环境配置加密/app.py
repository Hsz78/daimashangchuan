# from flask import Flask, jsonify
# from cryptography.fernet import Fernet

# # 密钥
# MASTER_KEY = "riK3qUGxf3wZDadTzqxhSz2vY7m2p0mCxnXmTrwT-Ck="

# # 加密后的密码
# ENCRYPTED_PWD = "gAAAAABp3fJi7wQdA6qbF-2lEH--NmCpmMvC8hhyEYAztvmgzqDS7j4hkfEVXcYK5t_tS8C2E1ZFiCWzbCi8pOWaOang8cNxzNjEdKgYajRsX6gBBOjeoNQ="

# app = Flask(__name__)

# # 解密
# fernet = Fernet(MASTER_KEY)
# real_pwd = fernet.decrypt(ENCRYPTED_PWD.encode()).decode()

# print("=====================================")
# print("加密密码:", ENCRYPTED_PWD)
# print("真实密码:", real_pwd)
# print("=====================================")

# @app.route('/env-check')
# def env_check():
#     return jsonify({
#         "env": "development",
#         "debug": True,
#         "数据库密码": real_pwd
#     })

# if __name__ == '__main__':
#     app.run()



from flask import Flask, jsonify
from cryptography.fernet import Fernet
import logging
from logging.handlers import RotatingFileHandler
import re

# ===================== 加密配置 =====================
MASTER_KEY = "riK3qUGxf3wZDadTzqxhSz2vY7m2p0mCxnXmTrwT-Ck="
ENCRYPTED_PWD = "gAAAAABp3fJi7wQdA6qbF-2lEH--NmCpmMvC8hhyEYAztvmgzqDS7j4hkfEVXcYK5t_tS8C2E1ZFiCWzbCi8pOWaOang8cNxzNjEdKgYajRsX6gBBOjeoNQ="

fernet = Fernet(MASTER_KEY)
real_pwd = fernet.decrypt(ENCRYPTED_PWD.encode()).decode()

# ===================== 日志脱敏过滤器 =====================
class SensitiveFilter(logging.Filter):
    def filter(self, record):
        msg = str(record.msg)
        # 隐藏手机号中间4位
        msg = re.sub(r'1[3-9]\d{9}', lambda m: m.group()[:3] + '****' + m.group()[-4:], msg)
        # 隐藏身份证
        msg = re.sub(r'\d{6}(\d{8})\d{4}', '******************', msg)
        # 隐藏密码
        msg = re.sub(r'(密码|password|pwd)[\s：=:]\w+', r'\1: ***', msg, flags=re.I)
        record.msg = msg
        return True

# ===================== 日志配置 =====================
def setup_logger():
    logger = logging.getLogger('flask_app')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    # 按大小切割日志：最多5个文件，每个10MB
    handler = RotatingFileHandler(
        'app.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    handler.addFilter(SensitiveFilter())  # 开启脱敏
    logger.addHandler(handler)
    return logger

logger = setup_logger()

# ===================== Flask 应用 =====================
app = Flask(__name__)

@app.route('/env-check')
def env_check():
    # 关键：这里一定要打日志！
    logger.info("用户访问了环境检查接口，手机号：13800138000，密码：123456")
    return jsonify({
        "env": "development",
        "debug": True,
        "数据库密码": real_pwd
    })

if __name__ == '__main__':
    logger.info("Flask 服务启动成功")
    app.run()