
# ---------------------------------------------------------------------------------------------------
import time
import json  # 讲获取的消息进行字典化
import socket  # 使用socket监听上报，接收各种消息
import requests  # 发送消息及获取机器人回答

SK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SK.bind(('127.0.0.1', 5720))  # 绑定IP及端口号
SK.listen(100)  # 开始监听
# 用来回复go-cqhttp上报，防止黄色的上报指令的输出，以及不可操控的程序错误(测试的错误：不停地回复消息)
HttpResponseHeader = '''HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'''

while True:
    Client, Address = SK.accept()  # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
    Reporting_events = Client.recv(1024).decode(encoding='utf-8')  # 主动初始化TCP服务器连接,并解码

    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))  # 完整发送TCP数据,并回复go-cqhttp的上报
    # print(Reporting_events)
    Client.close()  # 关闭连接

    # 用切片的方法把“{”找到，并获取后面的消息
    num = 0
    while True:
        num = num + 1
        # 用切片的方法把“{”找到，并获取后面的消息
        Processing_text = Reporting_events[num]
        if Processing_text == "{":
            Processed_text = Reporting_events[num:]
            print(Processed_text)
            break
        else:
            pass





