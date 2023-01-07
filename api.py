import main_api_program #大部分主要功能在此设计
import multi_group_shouting_api #多群喊话的api文件

# ---------------------------------------------------------------------------------------------------
#聊天回复函数
def Chat_reply():
    while True:
        #获取消息
        words = main_api_program.Listener().Preprocessing_segment(main_api_program.Listener().receiver())
        #print(word)
        #分离消息
        Group_private_chat = main_api_program.Detach_Message().group_separation(words)
        Other_chat = main_api_program.Detach_Message().Other_separation(words)
        #输出消息内容
        main_api_program.Send_operation().Send_operation_first()
        #多群喊话

        word = main_api_program.answer_logic().get_API_answer()

        multi_group_shouting_api.multi_group_shouting(word)
        main_api_program.Send_operation().Send_operation_second(word)
        #清除字典里的内容
        main_api_program.Clear_Dictionary().clear_()




if __name__ == '__main__':
    Chat_reply()



