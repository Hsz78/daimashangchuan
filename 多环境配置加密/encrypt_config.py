from cryptography.fernet import Fernet

# 直接用你刚才生成的 key
MASTER_KEY = "riK3qUGxf3wZDadTzqxhSz2vY7m2p0mCxnXmTrwT-Ck="
fernet = Fernet(MASTER_KEY)

# 要加密的密码
plain_pwd = "dev_password_123"

# 加密
encrypted = fernet.encrypt(plain_pwd.encode()).decode()
print("加密后的密码：", encrypted)