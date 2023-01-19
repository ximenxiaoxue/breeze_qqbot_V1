import requests

'''
music_name = "起风了"#str(input("歌曲名字:"))
artist = ""#str(input("可不填"))
'''
music_collect = []


def handle_content(word):  # handle:处理

    # 处理点歌的文字
    handle_after = word[2:]
    #print(handle_after)

    return handle_after


def music_id(handle_after):
    # 获取音乐的ID并弹出
    try:
        url = "http://cloud-music.pl-fe.cn/search?keywords={}".format(handle_after)
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
        res = requests.get(url=url, headers=headers).json()
        list = res["result"]['songs']
        # print(list)
        # print(list)
        liz = list[0]['id']
        for li in list:
            music_id = li['id']
            music_artists = li['artists'][0]["name"]
            UID = str(handle_after) + ":" + str(music_id) + ":" + str(music_artists)
            music_collect.append(UID)
            #print(UID)
        return liz
    except:
        msg = "遇到未知错误，准备记录错误消息以及时间"
        #print(msg)
        return msg


if __name__ == '__main__':
    music_id(handle_content("点歌平凡之路朴树"))
