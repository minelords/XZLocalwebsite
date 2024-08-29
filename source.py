import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
from fake_useragent import UserAgent
import os



   
#获取技术文章中心 
def get_topic():
    if not os.path.exists("source"):
        os.makedirs("source")
    headers={
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        "referer":"https://xz.aliyun.com"
    }
    for i in range(1,39):
        url="https://xz.aliyun.com/node/11?page={}".format(str(i))

        resp=requests.get(url,headers=headers)
        with open(f"source/{i}.html","w",encoding="utf-8") as f:
            f.write(resp.text)
            

#获取文章源码    
def get_article(driver,url):
    driver.get(url)
    time.sleep(0.5)
    source=driver.page_source
    return source


#配置浏览器
def init_dirver():
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")
    options.add_argument(f'user-agent={UserAgent().random}')
    driver=webdriver.Edge(options=options)
    return driver


def begin(pages):
    for p in pages:     
        with open('source/{}.html'.format(str(p)),'r',encoding='utf-8') as f:
            text=f.read()
        nums=re.findall(r'<a class="topic-title" href="/t/(.*?)">',text)
        #遍历源html
        source_path="source"
        source_names = os.listdir(source_path)
        source=[f.split(".")[0] for f in source_names]
        for num in nums:
            if num not in source:
                driver=init_dirver()
                url="https://xz.aliyun.com/t/{}".format(num)
                try:    
                    page_source=get_article(driver,url)
                except:
                    print("访问出错，请待会再试吧")
                    break
                with open(f'source/{num}.html','w',encoding='utf-8') as f:
                    f.write(page_source)
                driver.close()
            print(num,"was in source")
        print("所选页面下载完成")


if __name__=='__main__':
    #get_topic()
    pages=[1]
    begin(pages)