#!/usr/bin/env python3

import bcrypt #导入bcrypt模块

passwd_correct = b'123456'#密码
passwd_wrong = b'654321'

salt = bcrypt.gensalt() #生成随机盐
hashed = bcrypt.hashpw(passwd_correct, salt) #使用bcrypt模块进行加密
# hashed = bcrypt.hashpw(passwd_wrong, salt) #再次加密就会重新覆盖原本正确的密码所以后续的输出就会报错
print("生成的哈希值：", hashed)
# 验证正确密码
print("正确密码验证：", bcrypt.checkpw(passwd_correct, hashed))  # True
# 验证错误密码
print("错误密码验证：", bcrypt.checkpw(passwd_wrong, hashed))    # False
