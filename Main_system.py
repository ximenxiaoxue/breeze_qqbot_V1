#引用已编写好的聊天主程序
#这个为简单开头
import time

from api_basic import main_api_program #大部分主要功能在此设计
from api import multi_group_shouting_api #多群喊话的api文件
# ---------------------------------------------------------------------------------------------------
#聊天回复函数
def Chat_reply():
    while True:
        try:
            # 获取消息
            words = main_api_program.Listener().Preprocessing_segment(main_api_program.Listener().receiver())
            # print(word)
            # 分离消息
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

if __name__ == '__main__':
    Chat_reply()

