import datetime#检测新闻是否为最新
import re

import requests#获取内容
from bs4 import BeautifulSoup

def news_api():
    url = "https://www.163.com/dy/media/T1603594732083.html"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
    }

    res = requests.get(url=url, headers=headers).text
    #print(res)

    soup = BeautifulSoup(res, "lxml")
    #准备检查日期
    T = str(datetime.date.today())
    #获取日期以及新闻的url
    check_content = soup.select(" div.container.clearfix  div.content_box.wrap div.tab_content  ul  li:nth-child(1)  div  div  span")[0].string
    #print(check_content)

    if T in check_content:
        #print(1)
        #获取新闻的url
        url_news = soup.select(" div.container.clearfix div.tab_content  ul  li div  h4  a")[0].get("href")
        #print(url_news)
        res_news = requests.get(url=url_news, headers=headers).text
        soup = BeautifulSoup(res_news, "lxml")
        #定位到新闻的部分
        list = soup.select("#content  div.post_body p")#\31 FOR08TU > br
        #先把<br/>剔出来
        msg = str(list[1]).replace("<br/>","")

        #想着把新闻格式化一下，不过在这上面浪费掉的时间太多了，所以就不改了
        msg = re.findall(r'<p id="1FRCR35M">(.*)</p>', str(msg))[0]


        return msg
       #msg =re.match(r'<br/>(.*)<br/>')

    else:

        print(0)
        msg = "最新日期新闻，在网站暂未发布，请稍后再试"

    return None



    return None

if __name__ == '__main__':
    news_api()
