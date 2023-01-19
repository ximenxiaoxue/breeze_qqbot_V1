import requests
#https://api.aa1.cn/
#在此网站的api的调用聚合
#不得不说确实好用，整个api接口都给弄好了，只需要极少的代码量就可以实现接口的调用以及删除无用字符
#属实厉害
def wangyiyun():#实现网抑云热评_V1
    try:
        url = "https://v.api.aa1.cn/api/api-wenan-wangyiyunreping/index.php?aa1=json"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
        res = requests.get(url=url, headers=headers).json()
        msg = res[0]["wangyiyunreping"]
        #print(msg)
        return msg

    except:
        msg = "每日一言错误"
        return msg

def philosophy_of_life():#实现随机美句
    try:
        url = "https://zj.v.api.aa1.cn/api/wenan-mj/?type=json"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
        res = requests.get(url=url, headers=headers).json()
        msg = res["msg"]
        #print(msg)
        return msg
    except:
        msg = "每日一言错误"
        return msg

def i_counted_the_days_on_earth():#实现我在人间凑数的日子
    try:
        url = "https://v.api.aa1.cn/api/api-renjian/index.php?type=json"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"}
        res = requests.get(url=url, headers=headers).json()
        msg = res["renjian"]
        #print(msg)
        return msg
    except:
        msg = "每日一言错误"
        return msg



if __name__ == '__main__':
    i_counted_the_days_on_earth()




