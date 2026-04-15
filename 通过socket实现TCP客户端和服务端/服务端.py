import socket
#创建scoket对象
socket_server = socket.socket()
#绑定ip和端口
socket_server.bind(('localhost',8888))
# listen方法内接受一个整数传参数，表示接受的连接数量，可不填
socket_server.listen(1)

# 等待客户端连接，accept方法返回二元元组(连接对象, 客户端地址信息)
# accept()方法是阻塞式的方法，如果没有客户端连接，会一直等待，不往下执行
print(f"服务端已开始监听，正在等待客户端连接...")
conn, address = socket_server.accept()
print(f"接收到了客户端的连接，客户端的信息：{address}")
while True:
    # 接收消息
    data: str = conn.recv(1024).decode("UTF-8")
    print(f"客户端发来的消息是：{data}")
    # 回复消息
    msg = input("请输入你要回复客户端的消息：")
    if msg == 'exit':
        break
    conn.send(msg.encode("UTF-8"))  # encode将字符串编码为字节数组对象
conn.close()
socket_server.close()