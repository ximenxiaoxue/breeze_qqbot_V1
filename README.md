# breeze_qqbot
***
# 清风QQ机器人
使用go-cqhttp框架写成的简单QQ机器人
>本文讲解链接：http://t.csdn.cn/4dnAB

---

**最后附有各种上报**

**socket简单教程**：https://www.runoob.com/python3/python3-socket.html

**所有的文件都在这(包括config.yml)密码：博主好菜**：https://www.123pan.com/s/UovlVv-5P83h

**go-cqhttp下载**:https://docs.go-cqhttp.org/

go-cqhttp的config.yml文件改动了部分内容，如下所示，改动部分在这个文件的靠下的位置（或者直接用我的文件进行替换），将前面的“#”号删去，并在url中加上，

http://127.0.0.1:5720/

---

# 一.思路讲解
该怎么说呢，咱这个QQ机器人，就一个普通的单线程程序，所以**代码一多运行的就慢了**。

**正常的思路**
1. 等待消息出现
2. 接收消息，并做处理
3. 回复消息
4. 循环

这是一个最简单的思路，接下来咱就跟着这个最简单的思路，往下恰代码，我知道你们肯定喜欢敲代码

---

# 二.源代码讲解
这次咱们就不把源码放上了，源码都在上面大家可以下下来直接看，咱们直接进入主题。

## 1.main_api_program.py源码讲解
```
# Predetermined:预先确定   Specific:具体的
# Reporting:报告          directives：指令
# Preprocessing：预处理    instruction:指令
# segment：段
# Detach:拆卸
# Overall:全部
# separation:分离
# ---------------------------------------------------------------------------------------------------
print("正在进行预处理")
# ---------------------------------------------------------------------------------------------------
import time
t1 = time.time()

import json  # 讲获取的消息进行字典化
import socket  # 使用socket监听上报，接收各种消息
import pandas as pd  # 准备实现本地词库
import requests  # 发送消息及获取机器人回答
import news_api #实现新闻
import music_api#实现点歌
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
print("预处理完毕，用时:"+str((t2-t1)*1000)[:8]+"毫秒" )
```
感觉这些挺通俗易懂的，当然我相信你们是会的,况且我上面加了详细的注释..........................

好，直接及进入下一步
```
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
```
这里与之前不同，之前咱们的代码是靠的go-cqhttp的api指令进行获取的群消息，这次咱们使用的socket来获取消息，用socket的好处就是，可以接收到各种上报事件，消息就是上报事件之一，这样咱们也就可以进行回复私聊消息等各种的操作。

接下来跟着博主来看看运行的代码，当然就是单纯这里的运行代码
```
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
```

下面是运行的代码结果
```
POST / HTTP/1.1
Host: 127.0.0.1:5720
User-Agent: CQHttp/4.15.0
Content-Length: 386
Content-Type: application/json
X-Self-Id: 2712065523
Accept-Encoding: gzip

{"post_type":"meta_event","meta_event_type":"heartbeat","time":1673787352,"self_id":2712065523,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"packet_received":26,"packet_sent":17,"packet_lost":0,"message_received":0,"message_sent":0,"disconnect_times":0,"lost_times":0,"last_message_time":0}},"interval":5000}

{"post_type":"meta_event","meta_event_type":"heartbeat","time":1673787352,"self_id":2712065523,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"packet_received":26,"packet_sent":17,"packet_lost":0,"message_received":0,"message_sent":0,"disconnect_times":0,"lost_times":0,"last_message_time":0}},"interval":5000}
```
这里大家也都看见了，第一部分是
```
POST / HTTP/1.1
Host: 127.0.0.1:5720
User-Agent: CQHttp/4.15.0
Content-Length: 386
Content-Type: application/json
X-Self-Id: 2712065523
Accept-Encoding: gzip

{"post_type":"meta_event","meta_event_type":"heartbeat","time":1673787352,"self_id":2712065523,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"packet_received":26,"packet_sent":17,"packet_lost":0,"message_received":0,"message_sent":0,"disconnect_times":0,"lost_times":0,"last_message_time":0}},"interval":5000}
```
所以我们就想要拿到这第一部分的下面的内容，然后我就想了一个办法，用切片的方法把这里获取下来。


```
无消息
{"post_type":"meta_event","meta_event_type":"heartbeat","time":1673788242,"self_id":2712065523,"interval":5000,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"packet_received":59,"packet_sent":50,"packet_lost":0,"message_received":0,"message_sent":0,"disconnect_times":0,"lost_times":0,"last_message_time":0}}}
有消息
{"post_type":"message","message_type":"group","time":1673788243,"self_id":2712065523,"sub_type":"normal","font":0,"group_id":736038975,"message_seq":1805,"raw_message":"你好","anonymous":null,"message":"你好","sender":{"age":0,"area":"","card":"额额","level":"","nickname":"C-C（x_x；）","role":"owner","sex":"unknown","title":"","user_id":1732373074},"user_id":1732373074,"message_id":301654598}
```
所以在取消息的时候一定不要弄的太绝对 ，额，至于怎么绝对，就自己想吧，我反正是出错了。


好了，按照我们的思路，我们要拿到发送的消息，把没用的剔除去，毕竟是字典，我们用键值取值的方法就可以拿到消息的各个参数，并添加到我们设置的字典中，也就是咱们下面的代码。
```
class Detach_Message():
    # 精细化分离消息，准备实现私聊与群聊的回复
    def group_separation(self, Set_to_be_separated):

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

    def Other_separation(self, Set_to_be_separated):  # 其他消息的获取

        if Set_to_be_separated["post_type"] == "message":
            sender_msg = Set_to_be_separated["message"]  # 获取消息
            sender_name = Set_to_be_separated["sender"]["nickname"]  # 获取发送者的名字
            sender_id = Set_to_be_separated["sender"]["user_id"]  # 获取发送者的QQ号
            sender_msg_id = Set_to_be_separated["message_id"]  # 获取消息的ID
            sender_self_id = Set_to_be_separated["self_id"]  # 获取自己的QQ号
            # return sender_msg,sender_name,sender_id,sender_msg_id
            if Set_to_be_separated["message_type"] == "group":
                sender_group_id = Set_to_be_separated["group_id"]  # 获取发送群的群号

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
        
```
说实话，我也不知道为什么我当初要单独把判断消息的群聊还是私聊的取值要单独弄一个函数，算了不管了，直接摆烂，我相信你们这些大佬一定会解决好这些问题的，不想改的就勉强看着我的吧。

**以下是示例**
```
群聊
{"post_type":"message","message_type":"group","time":1673789105,"self_id":2712065523,"sub_type":"normal","anonymous":null,"font":0,"group_id":736038975,"raw_message":"在","sender":{"age":0,"area":"","card":"额额","level":"","nickname":"C-C（x_x；）","role":"owner","sex":"unknown","title":"","user_id":1732373074},"message":"在","message_seq":1806,"user_id":1732373074,"message_id":-1997294596}
私聊
{"post_type":"message","message_type":"private","time":1673789107,"self_id":2712065523,"sub_type":"friend","target_id":2712065523,"message":"在","raw_message":"在","font":0,"sender":{"age":0,"nickname":"C-C（x_x；）","sex":"unknown","user_id":1732373074},"message_id":-98257865,"user_id":1732373074}
```
好了，我们继续向下讲
```
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

    def Send_operation_second(self, msg, *age):  # 进行回复
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
```

好了，就这样吧，requests的使用不会的可以看一下前面的文章，我太懒了。
接下来，继续讲

```
class answer_logic():  # 回复逻辑
    # 逻辑回答，以后可能会再改，将判断分开，用多线程
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

        if dict_receive['sender_msg'] == "菜单" or dict_receive['sender_msg'] == "#":  # 回答消息的第二优先级

            msg = "1.聊天\n2.多群喊话\n3.新闻\n4.点歌(网抑云)\n5.网抑云\n6.随机美句\n7.我在人间凑数的日子"  # \n可以实现多行输出
            return msg

        elif dict_receive['sender_msg'] == "多群喊话" or dict_receive['sender_msg'] == "#2":  # 在此判断发消息人的QQ号
            if '1732373074' == dict_receive['sender_id']:  # 防止别人发送(有缺陷，如果主人先发多群喊话，不管谁再发消息，都会喊)
                msg = '接收消息中......'
                return msg
            else:
                msg = '您的等级不够'
                return msg

        elif dict_receive['sender_msg'] == "新闻" or dict_receive['sender_msg'] == "#3":
            msg = news_api.news_content()
            return msg

        elif "点歌" in dict_receive['sender_msg']:
            musics_id = music_api.music_id(music_api.handle_content(dict_receive['sender_msg']))
            msg = "[CQ:music,type=163,id={}]".format(musics_id)
            return msg

        elif dict_receive['sender_msg'] == "网抑云" or dict_receive['sender_msg'] == "#5":
            msg = api_group_1.wangyiyun()
            return msg

        elif dict_receive['sender_msg'] == "随机美句" or dict_receive['sender_msg'] == "#6":
            msg = api_group_1.philosophy_of_life()
            return msg

        elif dict_receive['sender_msg'] == "我在人间凑数的日子" or dict_receive['sender_msg'] == "#7":
            msg = api_group_1.i_counted_the_days_on_earth()
            return msg



        else:  # 回答消息的第三优先级

            urls = "http://api.qingyunke.com/api.php?key=free&appid=0&msg={}".format(dict_receive['sender_msg'])
            answer_get = requests.get(url=urls).json()
            answer_content = answer_get["content"]  # 获取API回答的内容
            # print('>>>:' * 3 + "回答：" + answer_content)  # 检察是否可以正常运行
            msg = answer_content
            return msg

```
那我们就继续向下讲了。
```
class Clear_Dictionary():  # 清除字典中的数据，后面有许多的地方需要清空字典
    def clear_(self):
        dict_receive['sender_msg'] = ''
        dict_receive['sender_name'] = ''
        dict_receive['sender_id'] = ''
        dict_receive['sender_msg_id'] = ''
        dict_receive['sender_group_id'] = ''
        dict_receive['message_type'] = ''
        dict_receive['sender_self_id'] = ''
```

## 2.Main_system.py源码讲解
```
#引用已编写好的聊天主程序
#这个为简单开头
import main_api_program #大部分主要功能在此设计
import multi_group_shouting_api #多群喊话的api文件
# ---------------------------------------------------------------------------------------------------
#聊天回复函数
def Chat_reply():
    while True:
        try:
            # 获取消息
            words = main_api_program.Listener().Preprocessing_segment(main_api_program.Listener().receiver())
            # print(word)
            # 分离消息
            Group_private_chat = main_api_program.Detach_Message().group_separation(words)
            Other_chat = main_api_program.Detach_Message().Other_separation(words)
            # 输出消息内容 输出的消息是获取的消息
            main_api_program.Send_operation().Send_operation_first()
            # 获得回答逻辑中的程序回答
            word = main_api_program.answer_logic().get_API_answer()
            # 多群喊话
            multi_group_shouting_api.multi_group_shouting(word)
            # 输出的消息是回答逻辑中的程序回答
            main_api_program.Send_operation().Send_operation_second(word)  # 多群喊话完后这里也会输出，不过是空
            # 清除字典里的内容
            main_api_program.Clear_Dictionary().clear_()
        except:
            print("-----" + "遇到未知错误！@#￥%……&*" + "-----")
            print("-----" + "记录错误！@#￥%……&*" + "-----")
            # main_api_program.Send_operation().Send_operation_second(main_api_program.answer_logic().failing_answer(),1)


if __name__ == '__main__':
    Chat_reply()
```
额，我认为不用讲了，注释已经很清楚了，额，单纯是我懒

# 三.最后
**文章写的肯定是不好，有错误希望大佬斧正**

**有不明白的可以留言，我会关注这些评论的，有不懂的可以看看go-cqhttp的官网，已经我的前面的文章，或者别的教程，总之，谢谢支持**

**也让我们，共同进步**

---


```
无消息
{"post_type":"meta_event","meta_event_type":"heartbeat","time":1673788242,"self_id":2712065523,"interval":5000,"status":{"app_enabled":true,"app_good":true,"app_initialized":true,"good":true,"online":true,"plugins_good":null,"stat":{"packet_received":59,"packet_sent":50,"packet_lost":0,"message_received":0,"message_sent":0,"disconnect_times":0,"lost_times":0,"last_message_time":0}}}
有消息
{"post_type":"message","message_type":"group","time":1673788243,"self_id":2712065523,"sub_type":"normal","font":0,"group_id":736038975,"message_seq":1805,"raw_message":"你好","anonymous":null,"message":"你好","sender":{"age":0,"area":"","card":"额额","level":"","nickname":"C-C（x_x；）","role":"owner","sex":"unknown","title":"","user_id":1732373074},"user_id":1732373074,"message_id":301654598}

群聊
{"post_type":"message","message_type":"group","time":1673789105,"self_id":2712065523,"sub_type":"normal","anonymous":null,"font":0,"group_id":736038975,"raw_message":"在","sender":{"age":0,"area":"","card":"额额","level":"","nickname":"C-C（x_x；）","role":"owner","sex":"unknown","title":"","user_id":1732373074},"message":"在","message_seq":1806,"user_id":1732373074,"message_id":-1997294596}
私聊
{"post_type":"message","message_type":"private","time":1673789107,"self_id":2712065523,"sub_type":"friend","target_id":2712065523,"message":"在","raw_message":"在","font":0,"sender":{"age":0,"nickname":"C-C（x_x；）","sex":"unknown","user_id":1732373074},"message_id":-98257865,"user_id":1732373074}

好友请求
{"post_type":"request","request_type":"friend","time":1674114285,"self_id":2712065523,"user_id":3552638520,"comment":"我是成全","flag":"1674114285000000"}
```
