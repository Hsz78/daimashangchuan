#单引号（'）：最典型的 SQL 注入元凶
#危害场景：当用户输入的单引号直接拼接到 SQL 语句中，会篡改 SQL 的语义。

# 假设用户输入的参数是：1' OR '1'='1
user_id = input("请输入用户ID：")  # 恶意输入：1' OR '1'='1
sql = f"SELECT * FROM users WHERE id = '{user_id}'"
# 最终拼接出的SQL变成：SELECT * FROM users WHERE id = '1' OR '1'='1'
# 结果：原本只想查ID=1的用户，却查出了所有用户数据

#这种是把你输入的内容直接拼接到SQL语句中，导致SQL语句被篡改，最终查出所有用户数据




# 防护方法
# 1. 使用参数化查询，让数据库自己处理单引号
import sqlite3
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

user_id = input("请输入用户ID：")
# 正确写法：用?作为占位符，参数单独传入
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
result = cursor.fetchall()

#简单来说，就是把SQL语句和参数分开，参数单独传入，让数据库自己处理单引号

# 单引号：主要引发 SQL 注入，核心防护是用参数化查询而非字符串拼接；
