"""
pip install
"""
"""
requests
pandas
lxml
bs4
openpyxl
"""
#需下载的python库
# ---------------------------------------------------------------------------------------------------
#//错误记录：以便后面的人修改时使用
#//1.若经常获取到最后一次消息多次，是没有及时清除字典的原因
# ---------------------------------------------------------------------------------------------------
import threading
import time

from api_basic import main_api_program #大部分主要功能在此设计
from api import multi_group_shouting_api #多群喊话的api文件
from api import kill_pid_system #linux进程保护
from api import news_api

num = 0
def Chat_reception():
    global num
    try:
        t1 = time.time()

        # 获取消息
        words = main_api_program.Listener().Preprocessing_segment(main_api_program.Listener().receiver())
        # print(words)
        # 分离消息
        Other_chat = main_api_program.Detach_Message().msg_separation(words)
        if Other_chat == False:
            pass
        else:
            # 输出消息内容 输出的消息是获取的消息
            sum_1 = threading.Thread(
                target=main_api_program.Send_operation().Send_operation_first())
            sum_1.start()
            # print(1)
            # 获得回答逻辑中的程序回答
            word = main_api_program.answer_logic().get_answer()
            # print(2)
            # 多群喊话
            multi_group_shouting_api.multi_group_shouting(word)
            # 输出的消息是回答逻辑中的程序回答
            sum_2 = threading.Thread(
                target=main_api_program.Send_operation().Send_operation_second(word))  # 多群喊话完后这里也会输出，不过是空
            sum_2.start()
            # 清除字典里的内容
            main_api_program.Clear_().clear_Dictionary_receive()

        t2 = time.time()
        print(str(t2 - t1)[:4] + "秒")

    except:
        num = num+1
        print("*****错误*****")
        if num == 6:
            kill_pid_system

def pretreatment():
    news_api.news_content()
    print("预处理完成")

if __name__ == '__main__':
    sub_news = threading.Thread(target=pretreatment())
    sub_news.start()
    while True:

        sub_Chat = threading.Thread(target=Chat_reception(), daemon=True)
        # Chat_reply()

        sub_Chat.start()
        # Chat_reply()
        #print("结束")

