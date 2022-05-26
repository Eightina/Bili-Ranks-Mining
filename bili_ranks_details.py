my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]
import http
from bs4 import BeautifulSoup
import requests
import time
 

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36',
    'Host':'httpbin.org'
}

url = 'https://www.bilibili.com/v/popular/rank/all?spm_id_from=333.851.b_7072696d61727950616765546162.3'
r = requests.get(url,headers)
r=r.text
arch=open('rank.txt','w',encoding="utf-8")
arch.write(r)
soup = BeautifulSoup(r,'lxml')

all_links=soup.find_all(href=True,class_="title")
pts=soup.find_all(class_='pts')
print(len(pts))
c_pts=[]
for i in pts:
    i=str(i)
    aa=int(i.find('"pts"><div>'))
    aa+=11
    bb=int(i.find('<',aa))
    c_pts.append(int(i[aa:bb]))

m=0

for i in all_links:
    m+=1
print(m)
storage=[]
for item in all_links:
    item=str(item)
    url=item[25:60]
    storage.append(url)

def relocated(data,charabefore,charaafter):
    aa=int(data.find(charabefore))
    aa+=1
    bb=data.find(charaafter,aa-1)

    data=int(data[aa:bb])
    return data



        

def relocated2(data):
    aa=int(data.find('</i>'))
    aa+=4
    bb=data.find('万',aa-1)
    data=float(data[aa:bb].replace(' ',''))
    return int(data*10000)


tagheat={'动画':10,'鬼畜':0.8,'国创':2.6,'美食':10,'生活':10,'数码':5.6,'舞蹈':5.2,'音乐':10,'影视':10,'游戏':10,'娱乐':10,'知识':10,'资讯':0.1,'时尚':10}
def get_details(url):
    r = requests.get(url,headers)
    r=r.text
    soup = BeautifulSoup(r,'lxml')

    fan=str(soup.find('span',class_="has-charge"))
    ss=int(fan.find('关注'))
    aa=int(fan.find('>',ss))
    aa+=1
    bb=fan.find('<',aa)
    fan=fan[aa:bb]
    if fan=='Non':
        fan=1
    else:
        fan=0
    


    view=str(soup.find('span',class_="view"))    
    view=relocated(view,"数",'"')

    like=str(soup.find('span',class_="like"))
    like=relocated(like,"数",'"')

    dm=str(soup.find('span',class_="dm"))
    dm=relocated(dm,"数",'"')

    coin=str(soup.find('span',class_="coin"))
    if coin.find('万')!=-1:
        coin=relocated2(coin)
    else:
        coin=relocated(coin,"数",'"')

    collect=str(soup.find('span',class_="collect"))
    if collect.find('万')!=-1:
        collect=relocated2(collect)
    else:
        collect=relocated(collect,"数",'"')

    share=str(soup.find('span',class_="share"))
    if share.find('万')==-1:
        aa=int(share.find('</i>'))
        aa+=4
        share=int(share[aa:aa+5])
    else:
        share=relocated2(share)
    
    m=0
    tag=soup.find_all('li',class_='tag')
    for i in tag:
        m=str(i)
        if 'channel-name' not in m:
            tag=m
            break
    aa=int(str(tag).find('span>'))
    aa+=5
    bb=int(str(tag).find('<',aa-1))
    tag=tag[aa:bb]
    tag=tagheat[tag]
    

    vtime=str(soup.find('div',class_="video-data"))
    aa=vtime.find('弹幕</span>')
    aa+=15
    bb=vtime.find('</',aa)
    vtime=vtime[aa:bb]
    rtime=time.time()
    vtime=time.mktime(time.strptime(vtime, '%Y-%m-%d %H:%M:%S'))
    deltatime=rtime-vtime

    return([view,like,dm,coin,collect,share,fan,deltatime,tag])

dataset=[]

rank=1

for url in storage:
    time.sleep(0.1)
    dataset.append([rank]+get_details('https://'+url)+[c_pts[rank-1]])
    rank+=1
print(len(dataset))

filename=time.asctime((time.localtime(time.time()))).replace(' ','_').replace(':','_')+'_bili_ranks_100.csv'

import csv

headers = ['rank','view','like','dm','coin','collect','share','fan','deltatime','tag','c_pts']

with open(filename,'w',newline='')as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(dataset)









