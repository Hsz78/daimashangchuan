import pymysql # 导入PyMySQL模块

# 配置你的MySQL信息（新增这4行变量）
MYSQL_USER = "root"          # 你的MySQL用户名
MYSQL_PASS = "123456"        # 你的MySQL密码
MYSQL_DB = "student_db"      # 要连接的数据库名
TABLE_NAME = "student_info"  # 要查询的表名

#这行是 “打通 Python 和 MySQL 的通道”，pymysql.connect()是 pymysql 提供的连接函数；
conn = pymysql.connect(host='127.0.0.1', user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB) 
# 创建游标对象
cur = conn.cursor()
#执行查询 SQL
cur.execute(f"SELECT * FROM {TABLE_NAME}")  # 替换查询的表名

# 打印查询结果
for r in cur:
    print(r)
# 关闭游标和连接
cur.close()
conn.close()