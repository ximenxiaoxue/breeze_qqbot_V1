from api_basic import main_api_program
def multi_group_shouting(word): #实现多群喊话
    while True:
        if word == '接收消息中......':
            while True:
                Message_replied = main_api_program.receive_messages().receive_()
                # 多群喊话
                main_api_program.Multi_group_shouting().Get_group_list()
                main_api_program.Multi_group_shouting().Shouting_realization(Message_replied)

                break
        else:
            pass
    # 启用多群喊话的中转站
        #main_api_program.Clear_Dictionary().clear_()  # 清除字典中的内容
        break




