# Predetermined:预先确定   Specific:具体的
# Reporting:报告          directives：指令
# Preprocessing：预处理    instruction:指令
# segment：段
# Detach:拆卸
# Overall:全部
# separation:分离
# ---------------------------------------------------------------------------------------------------
import threading

print("正在进行预处理")
# ---------------------------------------------------------------------------------------------------
import time
t1 = time.time()

import json  # 讲获取的消息进行字典化
import socket  # 使用socket监听上报，接收各种消息
import pandas as pd  # 准备实现本地词库
import requests  # 发送消息及获取机器人回答
from api import news_api  # 实现新闻
from api import music_api  # 实现点歌
from api import api_group_1  # 实现每日一言等
from queue import Queue

# ---------------------------------------------------------------------------------------------------
# 实现本地词库时使用

# path = 'words\word.xlsx'  # 本地词库路径
data_word = pd.read_excel("words/word.xlsx")
word_question = data_word.loc[:, 'question']  # 读取question内容
word_answer = data_word.loc[:, 'answer']  # 读取answer内容
total = data_word.shape[0]  # data.shape可以获取行，列的数
# ---------------------------------------------------------------------------------------------------
# 接收消息时使用

SK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SK.bind(('127.0.0.1', 5720))  # 绑定IP及端口号
SK.listen(100)  # 开始监听
# 用来回复go-cqhttp上报，防止黄色的上报指令的输出，以及不可操控的程序错误(测试的错误：不停地回复消息)
HttpResponseHeader = '''HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'''
# ---------------------------------------------------------------------------------------------------
# 发送消息
# 存放获取的各种消息，以后有必要可能需要将各个消息存放的内容分开
dict_receive = {'message_type': '', 'sender_msg': '', 'sender_name': '', 'sender_id': '', 'sender_msg_id': '',
                'sender_group_id': '', 'sender_self_id': ''}
# 用副本字典准备使用多线程，讲多群喊话与正常的聊天分隔开
dict_receive_copy = {'message_type': '', 'sender_msg': '', 'sender_name': '', 'sender_id': '', 'sender_msg_id': '',
                     'sender_group_id': '', 'sender_self_id': ''}

# ---------------------------------------------------------------------------------------------------
# 获取群的ID与名称，为了实现多群喊话做准备
group_id_list = []
group_name_list = []
# ---------------------------------------------------------------------------------------------------
t2 = time.time()
jdm = False  #使用这个判断多线程获取回答的继续执行

ans_msg = {"answer":""} #存放获取到的回答，确实找不到什么好的资源共享的方式了

print("预处理完毕，用时:" + str((t2 - t1) * 1000)[:8] + "毫秒")

# ---------------------------------------------------------------------------------------------------
# 在这里进行消息之间的同道连接，以及获得的消息的第一步处理，进行字典化
class Listener():  # 获取网页的json并获取消息

    def receiver(self):
        Client, Address = SK.accept()  # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
        Reporting_events = Client.recv(1024).decode(encoding='utf-8')  # 主动初始化TCP服务器连接,并解码

        Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))  # 完整发送TCP数据,并回复go-cqhttp的上报
        # print(Reporting_events)
        Client.close()  # 关闭连接
        return Reporting_events  # 弹出获取的上报文字

    def Preprocessing_segment(self, Preprocess_Text):  # 处理上报文字
        # 用切片的方法把“{”找到，并获取后面的消息
        num = 0
        while True:
            num = num + 1
            # 用切片的方法把“{”找到，并获取后面的消息
            Processing_text = Preprocess_Text[num]
            if Processing_text == "{":
                Processed_text = Preprocess_Text[num:]
                # print(Processed_text)
                break
            else:
                pass
        return json.loads(Processed_text)  # 将字符串转变为字典


# ---------------------------------------------------------------------------------------------------
# 精细化分离消息，准备实现私聊与群聊的回复
class Detach_Message():
    def msg_separation(self, Set_to_be_separated):  # 其他消息的获取

        if Set_to_be_separated["post_type"] == "message":
            sender_msg = Set_to_be_separated["message"]  # 获取消息
            sender_name = Set_to_be_separated["sender"]["nickname"]  # 获取发送者的名字
            sender_id = Set_to_be_separated["sender"]["user_id"]  # 获取发送者的QQ号
            sender_msg_id = Set_to_be_separated["message_id"]  # 获取消息的ID
            sender_self_id = Set_to_be_separated["self_id"]  # 获取自己的QQ号
            # return sender_msg,sender_name,sender_id,sender_msg_id
            if Set_to_be_separated["message_type"] == "group":
                dict_receive['message_type'] = 'group'
                sender_group_id = Set_to_be_separated["group_id"]  # 获取发送群的群号
                dict_receive['sender_msg'] = sender_msg
                dict_receive['sender_name'] = sender_name
                dict_receive['sender_id'] = str(sender_id)
                dict_receive['sender_msg_id'] = str(sender_msg_id)
                dict_receive['sender_group_id'] = str(sender_group_id)
                dict_receive['sender_self_id'] = str(sender_self_id)


                pass
            else:
                dict_receive['message_type'] = 'private'
                dict_receive['sender_msg'] = sender_msg
                dict_receive['sender_name'] = sender_name
                dict_receive['sender_id'] = str(sender_id)
                dict_receive['sender_msg_id'] = str(sender_msg_id)
                dict_receive['sender_self_id'] = str(sender_self_id)
                pass
        else:
            return False #为后面加快运行速度做铺垫

        return None





# ---------------------------------------------------------------------------------------------------
class Send_operation():  # 可视化获取的消息类别等
    def Send_operation_first(self):
        # 输出获取到的消息
        if dict_receive['message_type'] == 'private':
            print(
                '>>>:' * 3 + "获取:  \n" + "名字:  " + dict_receive['sender_name'] + '\n' + 'QQ号:  ' + dict_receive[
                    'sender_id'] + '\n' + "消息内容:  " +
                dict_receive[
                    'sender_msg'] + '\n' + '消息ID：' + dict_receive['sender_msg_id'])
            # Clear_Dictionary().clear_() #清除字典中的数据
            pass

        elif dict_receive['message_type'] == 'group':
            print(
                '>>>:' * 3 + "获取:  \n" + "名字:  " + dict_receive['sender_name'] + '\n' + 'QQ号:  ' + dict_receive[
                    'sender_id'] + '\n' + '群号:  ' + dict_receive['sender_group_id'] + '\n' + "消息内容:  " +
                dict_receive[
                    'sender_msg'] + '\n' + '消息ID: ' + dict_receive['sender_msg_id'])
            # Clear_Dictionary().clear_()#清除字典中的数据
            pass

        else:
            pass
            # print('>>>:' * 3 +'暂无消息')
        return None

    def Send_operation_second(self, msg):  # 进行回复
        # 输出逻辑回答的消息
        url = 'http://127.0.0.1:5700'
        if dict_receive['message_type'] == 'private':
            urls = url + "/send_private_msg?user_id=" + dict_receive['sender_id'] + '&' + 'message=' + msg
            answer_post_use = requests.post(url=urls).json()  # 发送消息
            print('>>>:' * 3 + "已回答:" + "\n " + msg)
            pass
        elif dict_receive['message_type'] == 'group':

            urls = url + '/send_group_msg?group_id=' + dict_receive['sender_group_id'] + '&' + "message=" + msg
            # print(urls)
            answer_post_use = requests.post(url=urls)  # 发送消息
            print('>>>:' * 3 + "\n" + "已回答:" + msg)
            pass

        else:
            # print(1)
            pass


# ---------------------------------------------------------------------------------------------------

class answer_logic():  # 回复逻辑
    # 逻辑回答，以后可能会再改，将判断分开，用多线程
    def get_API_answer_1(self):  # 本地词库一级回答
        # 回答消息的第一优先级
        # 放到前面提前处理
        global jdm
        num = 0
        for num in range(total):
            num = +num  # 前加的意思是先进行一次运行下一次再 +1
            answer_Pre_post = str(word_question[num])
            '''
            因为回答的消息在同行，所以后面也是num。
            因为xlsx里面的数字是int类型，我们获取的消息里面的数字是str
            所以要用str转化一下，这个漏洞我找了好久
            哭~~~~~。
            '''
            if dict_receive['sender_msg'] == answer_Pre_post:

                jdm = True
                msg = word_answer[num]
                ans_msg['answer'] = msg

                #return msg  # 弹出本地词库消息，便于下面发送
            else:
                jdm = False
                pass

    def get_API_answer_2(self):
        global jdm,news_api,ans_msg
        if jdm == True:
            pass
        else:
            if dict_receive['sender_msg'] == "菜单" or dict_receive['sender_msg'] == "/":  # 回答消息的第二优先级
                jdm = True
                msg = "1.聊天\n2.多群喊话\n3.新闻\n4.点歌(网抑云)\n5.网抑云\n6.随机美句\n7.我在人间凑数的日子"  # \n可以实现多行输出
                ans_msg['answer'] = msg

                # return msg

            elif dict_receive['sender_msg'] == "多群喊话" or dict_receive['sender_msg'] == "/2":  # 在此判断发消息人的QQ号
                if '1732373074' == dict_receive['sender_id']:  # 防止别人发送(有缺陷，如果主人先发多群喊话，不管谁再发消息，都会喊)

                    jdm = True
                    msg = '接收消息中......'
                    ans_msg['answer'] = msg
                    # return msg
                else:
                    jdm = True
                    msg = '您的等级不够'
                    ans_msg['answer'] = msg

                    # return msg

            elif dict_receive['sender_msg'] == "新闻" or dict_receive['sender_msg'] == "/3":

                jdm = True
                msg = news_api.news_content()
                ans_msg['answer'] = msg



                # return msg
            elif "点歌" in dict_receive['sender_msg']:

                jdm = True
                musics_id = music_api.music_id(music_api.handle_content(dict_receive['sender_msg']))
                msg = "[CQ:music,type=163,id={}]".format(musics_id)
                ans_msg['answer'] = msg

                # return msg

            elif dict_receive['sender_msg'] == "网抑云" or dict_receive['sender_msg'] == "/5":
                jdm = True
                msg = api_group_1.wangyiyun()
                ans_msg['answer'] = msg
                # return msg
            elif dict_receive['sender_msg'] == "随机美句" or dict_receive['sender_msg'] == "/6":

                jdm = True
                msg = api_group_1.philosophy_of_life()
                ans_msg['answer'] = msg
                # return msg

            elif dict_receive['sender_msg'] == "我在人间凑数的日子" or dict_receive['sender_msg'] == "/7":

                jdm = True
                msg = api_group_1.i_counted_the_days_on_earth()
                ans_msg['answer'] = msg

                # return msg

            else:  # 回答消息的第三优先级
                jdm = False
                # return None

    def get_API_answer_3(self):
        global jdm
        if jdm == False:
            urls = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={}".format(dict_receive['sender_msg'])
            answer_get = requests.get(url=urls).json()
            answer_content = answer_get["content"]  # 获取API回答的内容
            # print('>>>:' * 3 + "回答：" + answer_content)  # 检察是否可以正常运行
            msg = answer_content
            ans_msg['answer'] = msg
            #return msg
        else:
            pass


    def get_answer(self):#多线程进行寻找回答，加快速度
        global jdm
        print(1)
        jdm == False
        sunm_1 = threading.Thread(target=answer_logic().get_API_answer_1())
        sunm_2 = threading.Thread(target=answer_logic().get_API_answer_2())

        sunm_1.start()
        #sunm_1.join()
        sunm_2.start()
        #sunm_2.join()

        sunm_3 = threading.Thread(target=answer_logic().get_API_answer_3())
        sunm_3.start()
        #sunm_3.join()

        #ans_msg["answer"] = ""
        return str(ans_msg['answer'])

    def failing_answer(self):
        msg = "未知错误"
        return msg


# ---------------------------------------------------------------------------------------------------
class Clear_():  # 清除字典中的数据，后面有许多的地方需要清空字典
    def clear_Dictionary_receive(self):
        dict_receive['sender_msg'] = ''
        dict_receive['sender_name'] = ''
        dict_receive['sender_id'] = ''
        dict_receive['sender_msg_id'] = ''
        dict_receive['sender_group_id'] = ''
        dict_receive['message_type'] = ''
        dict_receive['sender_self_id'] = ''


# ---------------------------------------------------------------------------------------------------
class receive_messages(Send_operation):  # 多群喊话中转站，因为启动喊话程序需要等待主人发送消息所以便需要循环等待消息发送
    def receive_(self):

        while True:
            # 提示准备接收消息
            Send_operation().Send_operation_second(answer_logic().get_API_answer())

            Clear_().clear_Dictionary_receive()
            # 消息处理
            words = Listener().Preprocessing_segment(Listener().receiver())
            #Group_private_chat = Detach_Message().group_separation(words)
            Other_chat = Detach_Message().msg_separation(words)
            # 输出获取到的需要喊话的内容
            Send_operation().Send_operation_first()
            word = dict_receive['sender_msg']  # 获取要发送的消息
            # print(word)

            if word == '接收消息中......' or word == '':
                pass
            else:
                # Send_operation().Send_operation_second(word)
                Clear_().clear_Dictionary_receive()
                return word


# ---------------------------------------------------------------------------------------------------
class Multi_group_shouting():  # 实现多群喊话

    def Get_group_list(self):  # 获取群列表
        # 将列表清空，毕竟不清空下次就会再添加上，造成多次喊话
        group_id_list.clear()
        group_name_list.clear()

        url = 'http://127.0.0.1:5700/get_group_list'
        res = requests.get(url=url).json()
        message_group_list = res['data']

        for list in message_group_list:  # 将群添加到集合中
            group_id = list['group_id']
            group_name = list['group_name']
            # print(list['group_id'],list['group_name'])
            group_id_list.append(group_id)
            group_name_list.append(group_name)
            print(group_name, group_id, '已添加')
        return None

    def Shouting_realization(self, word):
        num = 0
        for list in group_id_list:
            url = 'http://127.0.0.1:5700/send_group_msg?group_id=' + str(list) + '&message=' + str(word)
            req = requests.post(url=url).text

            name_group = group_name_list[num]
            num = num + 1
            print(name_group, list, "已发送")
        return None


# ---------------------------------------------------------------------------------------------------
# 聊天回复函数
def Chat_reply():
    while True:
        # start = time.perf_counter()
        # 获取消息
        words = Listener().Preprocessing_segment(Listener().receiver())
        # print(word)
        # 分离消息
        Group_private_chat = Detach_Message().group_separation(words)
        Other_chat = Detach_Message().Other_separation(words)
        # 输出消息内容
        Send_operation().Send_operation_first()

        word = answer_logic().get_API_answer()
        Send_operation().Send_operation_second(word)
        Clear_Dictionary().clear_()
        # end = time.perf_counter()
        # print("运行时间为", round(end-start), 'seconds')
        # print(dict_receive)
        # print(w)


# ---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    Chat_reply()
