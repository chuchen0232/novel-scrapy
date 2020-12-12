#成品#封面到章節
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from time import sleep
import random
from opencc import OpenCC
from pyquery import PyQuery as pq
import md
from md import BH
cc = OpenCC('s2twp')

cover_url="https://www.hetubook.com/book2/44/index.html"
#cover_url=input("請輸入和圖書的封面url:")
start=1
#start=int(input("從第幾章開始抓(輸入數字ex.1，2...)"))-1

baseURL="https://www.hetubook.com"
user_agent =md.headerRnd()#"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3" 
opt = webdriver.ChromeOptions()
opt.add_argument('--user-agent=%s' % user_agent)
driver = webdriver.Chrome('chromedriver.exe',options=opt)#
driver.get(cover_url)

soup = BeautifulSoup(driver.page_source,'lxml') 
#書名
novel_name=soup.select("h2")
novelName=[cc.convert(i.get_text()) for i in novel_name][0]
print(novelName)

#建立novel資料夾
folder_path ='./{}/'.format(novelName)
if (os.path.exists(folder_path) == False): #判斷資料夾是否存在
    os.makedirs(folder_path) #Create folder
#novelcover
book_cover=soup.select(".book_info img")
coverURL=baseURL+[i.get("src") for i in book_cover][0]
r = requests.get(coverURL)
with open("{}cover.jpg".format(folder_path), "wb")as f:  #wb代表二進位
    f.write(r.content)
#outline.txt
book_detail=soup.select(".book_info")[0]
aa=pq(str(book_detail))
aa.remove('.nav')
book_tags=soup.select(".tag dd a")
bookTags=[i.get_text()for i in book_tags]
with open("{}0.小說簡介".format(folder_path),"w+",encoding="utf-8") as f:
    f.write("標籤:")
    for tag in bookTags:
        f.write("["+tag+"]")
    f.write("\n"+"書名:")
    for i in aa.items():
        f.write(i.text())


#collect chapter

chapters_url=soup.select("#dir a")#("#dir dd a")
chapterURLs=[]
for i in chapters_url:
    chapterURL=baseURL+i.get("href")
    chapterURLs+=[chapterURL]

for url in chapterURLs[start:]:
    ##抓取編號
    number=chapterURLs.index(url)+1#.split("/")[-1].split(".html")[0]

    driver.get(url)
    #driver.maximize_window()
    soup = BeautifulSoup(driver.page_source,'lxml') 
    #卷名
    novel_season=soup.select("#content h2")
    novelSeason=[i.get_text() for i in novel_season][0]
    #print(novelSeason)
    #卷名資料夾
    # SeasonPath=folder_path+novelSeason+"/"
    # if (os.path.exists(SeasonPath) == False): #判斷資料夾是否存在
    #         os.makedirs(SeasonPath) #Create folder
    #章節名
    novel_chapter=soup.select("#content .h2")
    novelChapter=[i.get_text() for i in novel_chapter][0]
    #print(novelChapter)

    ##清洗soup
    washed=["s","dfn","kbd","big"]
    for item in washed:
        for tag in soup.select(item):
            tag.extract()
    #小說內容
    novel_content=soup.find_all("div",{"style":"visibility: visible;"})#soup.select("#content div")
    while novel_content==[]:
        print("再次抓取")
        driver.get(url)
        sleep(5)
        #driver.maximize_window()
        soup = BeautifulSoup(driver.page_source,'lxml')
        novel_content=soup.find_all("div",{"style":"visibility: visible;"})#soup.select("#content div")


    ##寫入
    if novelSeason!=novelChapter:
        txtName=str(number)+"."+novelSeason+"-"+novelChapter#章節名稱
    else:
        txtName=str(number)+"."+novelSeason
    print(txtName)
    with open("{}{}.txt".format(folder_path,txtName),"w+",encoding="utf-8") as f:
        for i in novel_content:
            line=i.get_text("<bh>")
            if line=="":
                continue
            line=md.removeBH(line)
            f.write(line)
            f.write("\n\n")
driver.close()
print("所有工作結束")