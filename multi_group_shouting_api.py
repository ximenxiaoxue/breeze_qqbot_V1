
import main_api_program
def multi_group_shouting(): #实现多群喊话
    while True:
        #start = time.perf_counter()
        #获取消息
        words = main_api_program.Listener().Preprocessing_segment(main_api_program.Listener().receiver())
        #print(words)
        #print("eee")
        #分离消息
        Group_private_chat = main_api_program.Detach_Message().group_separation(words)
        Other_chat = main_api_program.Detach_Message().Other_separation(words)
        word = main_api_program.answer_logic().get_API_answer()  # 获取逻辑回复的内容
        if word == '接收消息中......':
            while True:
                Message_replied = main_api_program.receive_messages().receive_()
                # 多群喊话
                main_api_program.Multi_group_shouting().Get_group_list()
                main_api_program.Multi_group_shouting().Shouting_realization(Message_replied)
                if Message_replied != '接收消息中......':
                    break
        else:
            pass
    # 启用多群喊话的中转站
        main_api_program.Clear_Dictionary().clear_()  # 清除字典中的内容
        break


if __name__ == '__main__':
    multi_group_shouting()

