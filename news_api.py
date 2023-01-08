import datetime#检测新闻是否为最新
import time
import requests#获取内容
from bs4 import BeautifulSoup

def news_api():
    #t1 = time.time()
    url = "https://www.liulinblog.com/kuaixun"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36"
    }
    res = requests.get(url=url, headers=headers).text

    soup = BeautifulSoup(res, "lxml")

    t1 = datetime.date.today()
    t2 = str(t1.month).replace("0", "")
    t3 = str(t1.day).replace("0", "")

    check_content = soup.select(" div.entry-wrapper  header  h2 a")[0].string
    #print(check_content)

    if t2 in check_content and t3 in check_content:#检测日期
        # print(1)
        # 拿取新闻的url
        url_news = soup.select(" div.entry-wrapper  header  h2 a")[0].get("href")
        #print(url_news)
        # 获取新闻的内容
        res_news = requests.get(url=url_news, headers=headers).text

        soup = BeautifulSoup(res_news, "lxml")
        list = soup.select(" div  div  div.entry-content.u-text-format.u-clearfix  section section")
        #print(list)

        msg = str(list[0]).replace("<section>", "").replace("<p>", "").replace("</p>", "").replace("</section>", "")
            #print(msg)
        # print(list)
    else:
        msg = "最新日期新闻，在网站暂未发布，请稍后再试"
        #print("0")
    #t2 = time.time()
    #print((t2 - t1) * 1000)
    #print(msg)
    return msg


if __name__ == '__main__':
    news_api()