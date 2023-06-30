# -*- coding:utf-8 -*-
'''
不登陆只能浏览两页
'''
import requests,time,os
from random import randint
from bs4 import BeautifulSoup
import pandas as pd

def parse_html(html):
    soup = BeautifulSoup(html,'lxml')
    contents = soup.find_all('div',class_="magazine-senior-search-results-list")
    mycontents = contents[0].find_all('li')
    titles = []
    magazines = []
    abstracts = []
    authors = []
    for mycontent in mycontents:
        # 获取标题
        rawTitle = mycontent.find('div',class_='it-bold space-bottom-m10')
        title = rawTitle.get_text(" ",strip=True)
        titles.append(title)
        # 获取摘要
        rawAbstract = mycontent.find('div',class_="div-text-line-three itsmlink")
        abstract = rawAbstract.get_text(" ",strip=True)
        abstracts.append(abstract)
        # 获取期刊，IF，出版日期，DOI，作者
        raw = mycontent.find_all('div',class_="div-text-line-one it-new-gary")
        i = 1
        for r in raw:
            data = r.get_text(" ",strip=True)
            if (i % 2 ==0):
                authors.append(data)
            else:
                magazines.append(data)
            i+=1
    return titles,magazines,abstracts,authors
def save_info(file,titles,magazines,abstracts,authors):
    dataFrame = pd.DataFrame({"title":titles,"magazine":magazines,"author":authors,"abstract":abstracts})
    dataFrame.to_csv(file,index=False,sep=',')

url = 'https://www.x-mol.com/paper/search/q?'
keyword = input('请输入关键词进行查询：')
searchField = str(input("请确定搜索范围（0代表全部，1代表标题摘要，2代表作者）："))
year = str(input("请确定发表年份，范围在2015-2023，无值表示全部包含，输入2015时包含2015以前的文章："))
impactFactorStart = str(input("IF大于："))
impactFactorEnd = str(input("IF小于："))
payload = {
    "searchField":searchField,  #"0"代表全部，"1"代表标题摘要，"2"代表作者
    "option":keyword,
    "searchSort":"", #默认为按匹配度排序，可选“publishDate”
    "onlyOA":"", #默认关闭，可选"true"
    "year":year,
    "impactFactorStart":"",  #IF起点
    "impactFactorEnd":"",   #IF终点
    "selectSearchType":"0",
    "matchPhrase":"true"    #是否开启仅显示精准匹配的结果
}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'}
for i in range(1,3):
    payload.update({"pageIndex":str(i)})   #页码
    r = requests.get(url,params=payload,headers=headers)
    with open(keyword+str(i)+'.html','w',encoding='utf-8') as f:
        f.write(r.content.decode('utf-8'))
    time.sleep(randint(1,3))

for root,dirs,files in os.walk(r'C:\Users\宋颖\Desktop\Python_product\3.python_spider\3.x-mol\x-mol'):
    for file in files:
        if (os.path.splitext(file)[1]=='.html'):
            with open(file,'r',encoding='utf-8') as f:
                html = f.read()
                titles,magazines,abstracts,authors = parse_html(html)
                save_info(file+'.csv',titles,magazines,abstracts,authors)

print('搜索完成，数据已保存')