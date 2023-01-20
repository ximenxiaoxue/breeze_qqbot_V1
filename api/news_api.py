import datetime#检测新闻是否为最新
import re
import time
import requests#获取内容
from bs4 import BeautifulSoup

co_co = {"datetime":"","news":""}

def news_take():#此函数只管拿取新闻的内容
    try:
        url = "https://www.163.com/dy/media/T1603594732083.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
        }

        res = requests.get(url=url, headers=headers).text
        # print(res)

        soup = BeautifulSoup(res, "lxml")
        # 准备检查日期
        # 获取日期以及新闻的url
        check_content = soup.select(
            " div.container.clearfix  div.content_box.wrap div.tab_content  ul  li:nth-child(1)  div  div  span")[
            0].string
        # print(check_content)
        T = str(datetime.date.today())

        if T in check_content:
            # print(1)
            # 获取新闻的url
            url_news = soup.select(" div.container.clearfix div.tab_content  ul  li div  h4  a")[0].get("href")
            # print(url_news)
            res_news = requests.get(url=url_news, headers=headers).text
            soup = BeautifulSoup(res_news, "lxml")
            # 定位到新闻的部分
            list = soup.select("#content  div.post_body p")  # \31 FOR08TU > br
            # 先把<br/>剔出来
            msg = str(list[1]).replace("<br/>", "")
            # print(msg)

            # 想着把新闻格式化一下，不过在这上面浪费掉的时间太多了，所以就不改了
            msg = re.match(r'<p id="(.*)">(.*)</p>', str(msg))
            # print(msg)
            msg = str(msg.group(2))
            # print(msg)
            co_co['news'] = msg
            # print(co_co['news'])
            return msg
        # msg =re.match(r'<br/>(.*)<br/>')
        else:
            # print(0)
            msg = "最新日期新闻，在网站暂未发布，请稍后再试"
            if co_co['news'] == "" :
                co_co['news'] = msg
            else:
                pass

    except:
        msg = "新闻获取系统错误"
        return msg


def news_content():#判断是否去列表拿取还是网站拿取
    content = "最新日期新闻，在网站暂未发布，请稍后再试"

    news_time = str(datetime.date.today())
    #print(news_time)
    if news_time != co_co['datetime']: #先判断列表中的新闻是否为今天的
        co_co['datetime'] = news_time #将获取的时间放入字典

        news_take()#获取内容
        msg = co_co['news']
        #print(1)
        return msg

    else:
        if co_co['news'] == "" or co_co['news'] == content:
            news_take()
            msg = co_co['news']
            #print(2)
            return msg
        else:
            msg = co_co['news']
            #print(3)
            return msg

if __name__ == '__main__':
    print(news_content())
