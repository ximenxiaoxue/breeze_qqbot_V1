import datetime#检测新闻是否为最新
import time

import requests#获取内容
from bs4 import BeautifulSoup

url = "https://www.liulinblog.com/kuaixun"
headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36"
}
res = requests.get(url=url,headers=headers).text
#print(res)
#[<a href="https://www.liulinblog.com/166011.html" rel="bookmark" target="_blank" title="1月8日，星期日，在这里每天60秒读懂世界！">1月8日，星期日，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165972.html" rel="bookmark" target="_blank" title="1月7日，星期六，在这里每天60秒读懂世界！">1月7日，星期六，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165926.html" rel="bookmark" target="_blank" title="1月6日，星期五，在这里每天60秒读懂世界！">1月6日，星期五，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165907.html" rel="bookmark" target="_blank" title="1月5日，星期四，在这里每天60秒读懂世界！">1月5日，星期四，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165880.html" rel="bookmark" target="_blank" title="1月4日，农历  腊月十三 星期三，在这里每天60秒读懂世界！">1月4日，农历  腊月十三 星期三，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165874.html" rel="bookmark" target="_blank" title="1月3日，星期二，在这里每天60秒读懂世界！">1月3日，星期二，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165872.html" rel="bookmark" target="_blank" title="1月2日，农历  腊月十一 星期一，在这里每天60秒读懂世界！">1月2日，农历  腊月十一 星期一，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165852.html" rel="bookmark" target="_blank" title="12月31日，农历  腊月初九 星期六，在这里每天60秒读懂世界！">12月31日，农历  腊月初九 星期六，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165820.html" rel="bookmark" target="_blank" title="12月30日，星期五，在这里每天60秒读懂世界！">12月30日，星期五，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165803.html" rel="bookmark" target="_blank" title="12月29日，星期四，在这里每天60秒读懂世界！">12月29日，星期四，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165780.html" rel="bookmark" target="_blank" title="12月28日，星期三，在这里每天60秒读懂世界！">12月28日，星期三，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165757.html" rel="bookmark" target="_blank" title="12月27日，星期二，在这里每天60秒读懂世界！">12月27日，星期二，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165731.html" rel="bookmark" target="_blank" title="12月26日，星期一，在这里每天60秒读懂世界！">12月26日，星期一，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165693.html" rel="bookmark" target="_blank" title="12月25日，星期日，在这里每天60秒读懂世界！">12月25日，星期日，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165661.html" rel="bookmark" target="_blank" title="12月24日，星期六，在这里每天60秒读懂世界！">12月24日，星期六，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165605.html" rel="bookmark" target="_blank" title="12月23日，星期五，在这里每天60秒读懂世界！">12月23日，星期五，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165591.html" rel="bookmark" target="_blank" title="12月22日，星期四，在这里每天60秒读懂世界！">12月22日，星期四，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165559.html" rel="bookmark" target="_blank" title="12月21日，星期三，在这里每天60秒读懂世界！">12月21日，星期三，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165544.html" rel="bookmark" target="_blank" title="12月20日，星期二，在这里每天60秒读懂世界！">12月20日，星期二，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/165496.html" rel="bookmark" target="_blank" title="12月19日，星期一，在这里每天60秒读懂世界！">12月19日，星期一，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/166013.html" rel="bookmark" target="_blank" title="互联网早报 | 1月8日 星期日 | 马云退出蚂蚁集团实控人位置；特斯拉国产车型大幅降价；亚马逊将裁撤超1.8万个岗位">互联网早报 | 1月8日 星期日 | 马云退出蚂蚁集团实控人位置；特斯拉国产车型大幅降价；亚马逊将裁撤超1.8万个岗位</a>, <a href="https://www.liulinblog.com/166011.html" rel="bookmark" target="_blank" title="1月8日，星期日，在这里每天60秒读懂世界！">1月8日，星期日，在这里每天60秒读懂世界！</a>, <a href="https://www.liulinblog.com/166006.html" rel="bookmark" target="_blank" title="雷婷2007-2019年55张专辑歌曲合集[WAV/33.47GB]百度云网盘下载">雷婷2007-2019年55张专辑歌曲合集[WAV/33.47GB]百度云网盘下载</a>, <a href="https://www.liulinblog.com/166001.html" rel="bookmark" target="_blank" title="2017-2021年198首歌曲合集[FLAC/MP3/1.05GB]百度云网盘下载">2017-2021年198首歌曲合集[FLAC/MP3/1.05GB]百度云网盘下载</a>, <a href="https://www.liulinblog.com/26267.html" rel="bookmark" target="_blank" title="考研英文外刊推荐：十大英文外刊，精读英文外刊文章汇总 百度云盘资源">考研英文外刊推荐：十大英文外刊，精读英文外刊文章汇总 百度云盘资源</a>, <a href="https://www.liulinblog.com/143632.html" rel="bookmark" target="_blank" title="勺子课堂全套课程155部视频合集百度云网盘下载">勺子课堂全套课程155部视频合集百度云网盘下载</a>, <a href="https://www.liulinblog.com/142110.html" rel="bookmark" target="_blank" title="源靖《女神聊天课》系列教程音频合集百度网盘下载">源靖《女神聊天课》系列教程音频合集百度网盘下载</a>, <a href="https://www.liulinblog.com/163583.html" rel="bookmark" target="_blank" title="【免费资源】黑亚当韩版1080P高清神秘代码（速存24小时必删）">【免费资源】黑亚当韩版1080P高清神秘代码（速存24小时必删）</a>, <a href="https://www.liulinblog.com/64004.html" rel="bookmark" target="_blank" title="win10系统怎么开启3d（win10游戏3d设置）">win10系统怎么开启3d（win10游戏3d设置）</a>, <a href="https://www.liulinblog.com/164262.html" rel="bookmark" target="_blank" title="BBC纪录片《铁路漫步》六集视频高清合集[MKV/5.09GB]百度云网盘下载">BBC纪录片《铁路漫步》六集视频高清合集[MKV/5.09GB]百度云网盘下载</a>]

soup = BeautifulSoup(res,"lxml")

t1 = datetime.date.today()
t2 = str(t1.month).replace("0","")
t3 = str(t1.day).replace("0","")

check_content = soup.select(" div.entry-wrapper  header  h2 a")[0].string
print(check_content)
t1 = time.time()
if t2 in check_content and t3 in check_content:
    #print(1)
    #拿取新闻的url
    url_news = soup.select(" div.entry-wrapper  header  h2 a")[0].get("href")
    print(url_news)
    #获取新闻的内容
    res_news = requests.get(url=url_news,headers=headers).text

    soup = BeautifulSoup(res_news, "lxml")
    list = soup.select(" div  div  div.entry-content.u-text-format.u-clearfix  section section")
    for li in list:
        print(str(li).replace("<section>","").replace("<p>","").replace("</p>","").replace("</section>",""))
    #print(list)
else:
    print("0")
t2 = time.time()
print((t2-t1)*1000)



