# 空值（None / 空字符串 ""）：程序崩溃 / 逻辑异常
# 危害场景：代码未处理空值时，会触发AttributeError、TypeError等异常，或导致业务逻辑出错。

# 假设用户输入的用户名是空字符串
username = input("请输入用户名：")  # 输入：（空）
# 直接调用字符串方法，若为空则逻辑异常；若为None则直接报错
if username.strip() == "admin":  # 空字符串strip()后还是空，逻辑不符；None会报AttributeError
    print("欢迎管理员")
else:
    print("普通用户")
#简单来说，就是没有对空值进行处理，导致程序崩溃，直接程序报错

# 防护方法
# 1.入参校验：检查是否为空值
# 2.设置默认值：避免空值引发异常

username = input("请输入用户名：").strip()  # 先去除首尾空格

# 校验空值
if not username:  # 空字符串/None都会返回True
    print("用户名不能为空！")
elif username == "admin":
    print("欢迎管理员")
else:
    print(f"欢迎{username}")
    
#空值：主要引发程序异常 / 逻辑错误，核心防护是入参校验 + 默认值处理；