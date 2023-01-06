import main_api_program


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

        word = main_api_program.answer_logic().get_API_answer()
        main_api_program.Send_operation().Send_operation_second(word)
        #清除字典里的内容
        main_api_program.Clear_Dictionary().clear_()








