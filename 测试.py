import socket
import json


SK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SK.bind(('127.0.0.1', 5720))  # 绑定IP及端口号
SK.listen(100)  # 开始监听
HttpResponseHeader = '''HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'''


Client, Address = SK.accept()  # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
Reporting_events = Client.recv(1024).decode(encoding='utf-8')  # 主动初始化TCP服务器连接,并解码

Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))  # 完整发送TCP数据,并回复go-cqhttp的上报
        # print(Reporting_events)
Client.close()  # 关闭连接


# 处理上报文字
# 用切片的方法把“{”找到，并获取后面的消息
num = 0
while True:
    num = num + 1
    # 用切片的方法把“{”找到，并获取后面的消息
    Processing_text = Reporting_events[num]
    if Processing_text == "{":
        Processed_text = Reporting_events[num:]

        break
    else:
        pass

print(Reporting_events)
print(Processed_text)
