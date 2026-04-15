from cryptography.fernet import Fernet
from decouple import config

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    JSON_SORT_KEYS = False

    # 解密方法
    @classmethod
    def decrypt_password(cls, encrypted_text):
        key = config('MASTER_KEY').encode()
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_text.encode()).decode()
"""
1. class BaseConfig:
这是一个配置父类，意思是：开发、测试、生产三套环境，共同的配置都放这里。后面三个环境的配置类，都会继承它，不用重复写。
2. SQLALCHEMY_TRACK_MODIFICATIONS = False
这是 Flask-SQLAlchemy 的配置
作用：关闭 “对象修改跟踪”
为什么关？
开着会额外占用内存，而且会弹出烦人的警告
实际项目几乎都关
3. SESSION_COOKIE_HTTPONLY = True
浏览器 Cookie 里的会话 ID，只允许浏览器访问，不允许 JavaScript 读取
作用：防 XSS 攻击
别人就算注入脚本，也拿不到你的登录状态
4. JSON_SORT_KEYS = False
Flask 默认会把返回的 JSON 按键名排序
设为 False → JSON 保持你写的顺序不变
好处：接口返回更清晰，调试更舒服
"""