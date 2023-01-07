# Predetermined:预先确定   Specific:具体的
# Reporting:报告          directives：指令
# Preprocessing：预处理    instruction:指令
# segment：段
# Detach:拆卸
# Overall:全部
# separation:分离
# ---------------------------------------------------------------------------------------------------
import requests  # 发送消息及获取机器人回答
import pandas as pd  # 准备实现本地词库
import time
import socket  # 使用socket监听上报，接收各种消息
import json

# ---------------------------------------------------------------------------------------------------
# 实现本地词库时使用

#path = 'words\word.xlsx'  # 本地词库路径
data_word = pd.read_excel("words/word.xlsx")
word_question = data_word.loc[:, 'question']  # 读取question内容
word_answer = data_word.loc[:, 'answer']  # 读取answer内容
total = data_word.shape[0]  # data.shape可以获取行列的总数
# ---------------------------------------------------------------------------------------------------
# 接收消息时使用

SK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SK.bind(('127.0.0.1', 5720))  # 绑定IP及端口号
SK.listen(100)  # 开始监听
# 用来回复go-cqhttp上报
HttpResponseHeader = '''HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'''
# ---------------------------------------------------------------------------------------------------
# go-cqhttp各种语法操作所需的指令

instruction = {'private': '/send_private_msg?', 'group': '/send_group_msg?', 'pd': 'user_id=', 'gd': 'group_id=',
               'msg': 'message='}  # 发送消息
dict_receive = {'message_type':'','sender_msg':'', 'sender_name':'', 'sender_id':'', 'sender_msg_id':'','sender_group_id':'','sender_self_id':''}
# ---------------------------------------------------------------------------------------------------
#获取群的ID与名称
group_id_list = []
group_name_list = []
# ---------------------------------------------------------------------------------------------------
class Listener():  # 获取网页的json并获取消息

    def receiver(self):
        Client, Address = SK.accept()  # 被动接受TCP客户端连接,(阻塞式)等待连接的到来
        Reporting_events = Client.recv(1024).decode(encoding='utf-8')  # 主动初始化TCP服务器连接,并解码

        Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))  # 完整发送TCP数据,并回复go-cqhttp的上报
        #print(Reporting_events)
        Client.close()  # 关闭连接
        return Reporting_events  # 弹出获取的上报文字

    def Preprocessing_segment(self,Preprocess_Text):  # 处理上报文字
        num = 0
        while True:
            num = num + 1
            # 用切片的方法把“{”找到，并获取后面的消息
            Processing_text = Preprocess_Text[num]
            if Processing_text == "{":
                Processed_text = Preprocess_Text[num:]
                #print(Processed_text)
                break
            else:
                pass
        return json.loads(Processed_text)#将字符串转变为字典

# ---------------------------------------------------------------------------------------------------
class Detach_Message():
    # 精细化分离消息，准备实现私聊与群聊的回复
    def group_separation(self,Set_to_be_separated):

        # 判断群私聊
        if Set_to_be_separated["post_type"] == "message":
            if Set_to_be_separated["message_type"] == "group":
                dict_receive['message_type'] = 'group'
                return None

            elif Set_to_be_separated["message_type"] == "private":
                dict_receive['message_type'] = 'private'
                return None

            else:
                pass
        else:  # 因为发送新消息时监听的消息集合与没有消息时的集合，不一样！！！！！！！！
            pass
        return None

    def Other_separation(self,Set_to_be_separated):#其他消息的获取

        if Set_to_be_separated["post_type"] == "message":
            sender_msg = Set_to_be_separated["message"] #获取消息
            sender_name = Set_to_be_separated["sender"]["nickname"]#获取发送者的名字
            sender_id= Set_to_be_separated["sender"]["user_id"] #获取发送者的QQ号
            sender_msg_id = Set_to_be_separated["message_id"] #获取消息的ID
            sender_self_id = Set_to_be_separated["self_id"]  #获取自己的QQ号
            #return sender_msg,sender_name,sender_id,sender_msg_id
            if Set_to_be_separated["message_type"] == "group":
                sender_group_id = Set_to_be_separated["group_id"] #获取发送群的群号

                dict_receive['sender_msg'] = sender_msg
                dict_receive['sender_name'] = sender_name
                dict_receive['sender_id'] = str(sender_id)
                dict_receive['sender_msg_id'] = str(sender_msg_id)
                dict_receive['sender_group_id'] = str(sender_group_id)
                dict_receive['sender_self_id'] = str(sender_self_id)

                pass
            else:
                dict_receive['sender_msg'] = sender_msg
                dict_receive['sender_name'] = sender_name
                dict_receive['sender_id'] = str(sender_id)
                dict_receive['sender_msg_id'] = str(sender_msg_id)
                dict_receive['sender_self_id'] = str(sender_self_id)
                pass
        else:
            pass

        return None

'''    def __init__(self, ):
        self.word = Set_to_be_separated
        print(self.word)
'''
# ---------------------------------------------------------------------------------------------------
class Send_operation():#可视化获取的消息类别等
    def Send_operation_first(self):

        if dict_receive['message_type'] == 'private':
            print(
                '>>>:' * 3 + "获取:\n" + dict_receive['sender_name'] + '\n' + 'QQ号:' + dict_receive['sender_id'] + '\n' +
                dict_receive[
                    'sender_msg'] + '\n' + '消息ID：' + dict_receive['sender_msg_id'])
            #Clear_Dictionary().clear_() #清除字典中的数据
            pass

        elif dict_receive['message_type'] == 'group':
            print(
                '>>>:' * 3 + "获取:\n" + dict_receive['sender_name'] +'\n' +'QQ号:' + dict_receive['sender_id'] + '\n'+'群号:'+dict_receive['sender_group_id']+'\n'+dict_receive[
                    'sender_msg'] + '\n'+'消息ID:' + dict_receive['sender_msg_id'])
            #Clear_Dictionary().clear_()#清除字典中的数据
            pass

        else:
            pass
            #print('>>>:' * 3 +'暂无消息')
        return None

    def Send_operation_second(self,msg):  # 进行回复
        url = 'http://127.0.0.1:5700'
        if dict_receive['message_type'] == 'private':
            urls = url + instruction['private'] + instruction['pd'] + dict_receive['sender_id'] + '&'+instruction['msg'] + msg
            answer_post_use = requests.post(url=urls).json()  # 发送消息
            print('>>>:' * 3 + "已回答:"+msg)
            pass
        elif dict_receive['message_type'] == 'group':

            urls = url + instruction['group'] + instruction['gd'] + dict_receive['sender_group_id'] + '&'+instruction['msg'] + msg
            #print(urls)
            answer_post_use = requests.post(url=urls).json()  # 发送消息
            print('>>>:' * 3 + "已回答:" + msg)
            pass
        else:
            pass

'''
        urls = "http://127.0.0.1:5700/send_group_msg?group_id=" + group_id + "&message=" + str(msg)
        answer_post_use = requests.post(url=urls).json()  # 发送消息
        print('>>>:' * 3 + "已回答")
'''

# ---------------------------------------------------------------------------------------------------
class answer_logic():#回复逻辑

    def get_API_answer(self):  # 本地词库一级回答
        # 回答消息的第一优先级
        # 放到前面提前处理

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
                msg = word_answer[num]

                return msg  # 弹出本地词库消息，便于下面发送
            else:
                pass

        if dict_receive['sender_msg'] == "菜单":  # 回答消息的第二优先级

            msg = "聊天\n多群喊话\n继续加油"#\n可以实现多行输出
            return msg
        elif dict_receive['sender_msg'] == "多群喊话" :
            if '1732373074' == dict_receive['sender_id']:
                msg = '接收消息中......'
                return msg
            else:
                msg = '您的等级不够'
                return msg

        else:  # 回答消息的第三优先级

            urls = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={}".format(dict_receive['sender_msg'])
            answer_get = requests.get(url=urls).json()
            answer_content = answer_get["content"]  # 获取API回答的内容
            #print('>>>:' * 3 + "回答：" + answer_content)  # 检察是否可以正常运行
            msg = answer_content
            return msg


# ---------------------------------------------------------------------------------------------------
class Clear_Dictionary():#清除字典中的数据
    def clear_(self):
        dict_receive['sender_msg'] = ''
        dict_receive['sender_name'] = ''
        dict_receive['sender_id'] = ''
        dict_receive['sender_msg_id'] =''
        dict_receive['sender_group_id'] =''
        dict_receive['message_type'] = ''
        dict_receive['sender_self_id'] = ''
# ---------------------------------------------------------------------------------------------------
class receive_messages(Send_operation):#多群喊话中转站
    def receive_(self):

        while True:
            #提示准备接收消息
            Send_operation().Send_operation_second(answer_logic().get_API_answer())

            Clear_Dictionary().clear_()
            #消息处理
            words = Listener().Preprocessing_segment(Listener().receiver())
            Group_private_chat = Detach_Message().group_separation(words)
            Other_chat = Detach_Message().Other_separation(words)

            Send_operation().Send_operation_first()
            word = dict_receive['sender_msg']#获取要发送的消息
            #print(word)

            if word == '接收消息中......' or word == '' :
                pass
            else:
                #Send_operation().Send_operation_second(word)
                Clear_Dictionary().clear_()
                return word
# ---------------------------------------------------------------------------------------------------
class  Multi_group_shouting(): #实现多群喊话

    def Get_group_list(self):#获取群列表
        #将列表清空，毕竟不清空下次就会再添加上，造成多次喊话
        group_id_list.clear()
        group_name_list.clear()

        url = 'http://127.0.0.1:5700/get_group_list'
        res = requests.get(url=url).json()
        message_group_list = res['data']

        for list in message_group_list:#将群添加到集合中
            group_id = list['group_id']
            group_name = list['group_name']
            # print(list['group_id'],list['group_name'])
            group_id_list.append(group_id)
            group_name_list.append(group_name)
            print(group_name, group_id, '已添加')
        return None

    def Shouting_realization(self,word):
        num = 0
        for list in group_id_list:
            url = 'http://127.0.0.1:5700/send_group_msg?group_id=' + str(list) + '&message=' + str(word)
            req = requests.post(url=url).text

            name_group = group_name_list[num]
            num = num + 1
            print(name_group, list, "已发送")
        return None


# ---------------------------------------------------------------------------------------------------
#聊天回复函数
def Chat_reply():
    while True:
        #start = time.perf_counter()
        #获取消息
        words = Listener().Preprocessing_segment(Listener().receiver())
        #print(word)
        #分离消息
        Group_private_chat = Detach_Message().group_separation(words)
        Other_chat = Detach_Message().Other_separation(words)
        #输出消息内容
        Send_operation().Send_operation_first()

        word =answer_logic().get_API_answer()
        Send_operation().Send_operation_second(word)
        Clear_Dictionary().clear_()
        #end = time.perf_counter()
        #print("运行时间为", round(end-start), 'seconds')
        #print(dict_receive)
        #print(w)


# ---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    Chat_reply()



