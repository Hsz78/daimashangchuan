#!/usr/bin/env python3

# import bcrypt #导入bcrypt模块

# passwd = b'123456'#密码

# salt = bcrypt.gensalt() #生成随机盐
# hashed = bcrypt.hashpw(passwd, salt) #使用bcrypt模块进行加密

# print(salt) #输出盐
# print(hashed) #输出加密后的密码
#请注意，盐是生成的哈希值的第一部分。 
#还要注意，每次生成唯一的 salt 和哈希值。 
#每次的哈希值都不一样，即使使用相同的密码和 salt 。


#!/usr/bin/env python3

import bcrypt

passwd = b's$cret12'

salt = bcrypt.gensalt()#生成随机盐
hashed = bcrypt.hashpw(passwd, salt)#加密

if bcrypt.checkpw(passwd, hashed):
    print("match")
else:
    print("does not match")

