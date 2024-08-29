import re
import os
import requests
import time

def download(text,img_names):
    headers={
        "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36",
        "referer":"https://xz.aliyun.com"
    }
    urls=re.findall(r'<img.*?src="(.*?)"',text)
    for url in urls:
        resp=requests.get(url,headers=headers)
        name=url.split("/")[-1]
        #如果页面中不存在此图片的话：
        if name not in img_names:
            print(name)
            if resp.status_code == 200:
            # 打开文件以二进制写入模式保存图片
                if not os.path.exists("output"):
                    os.makedirs("output")
                with open(f'output/static/img/{name}', 'wb') as file:
                    file.write(resp.content)
                print('Image downloaded successfully.')
            else:
                print('Failed to download image.')
        
        

def subtext(text,num):
    #修改跳转
    article=re.findall(r'href="/t/(.*?)"',text)
    for match in article:
        full_match = f'/t/{match}'
        text = re.sub(re.escape(full_match), f'{match}.html', text)
    
    #修改上下页
    page=re.findall(r'<a href="\?page=(.*?)">',text)
    for match in page:
        full_match = f'?page={match}'
        text = re.sub(re.escape(full_match), f'{match}.html', text)
    
    #剔除css,js
    t=re.findall(r'href="/static(/.*)/.*?"',text)

    for match in t:
        full_match = f'/static{match}'
        text = re.sub(re.escape(full_match), './static', text)

    text=text.replace('href="/static/bootstrap.min.css"','href="./static/bootstrap.min.css"')
    #剔除picture
    i=re.findall(r'img src="(.*)/.*?"',text)

    for match in i:
        full_match = f'{match}'
        text = re.sub(re.escape(full_match), './static/img', text)


    if not os.path.exists("output"):
        os.makedirs("output")
    with open(f"output/{num}.html",'w',encoding='utf-8') as f:
        f.write(text)



def spiderALL(dl=True):
    #遍历输出html       
    output_path="output"
    output_names = os.listdir(output_path)
    output=[f.split(".")[0] for f in output_names]


    #遍历源html
    source_path="source"
    source_names = os.listdir(source_path)
    source=[f.split(".")[0] for f in source_names]



    #遍历下载完毕的图片
    folder_path="output/static/img"
    img_names = os.listdir(folder_path)

    for num in source:
        if num not in output:
            with open(f'source/{num}.html','r',encoding='utf-8') as f:
                text=f.read()
                subtext(text,num)
                if dl==True:
                    download(text,img_names)


def spiderSingle(num):
    with open(f'source/{str(num)}.html','r',encoding='utf-8') as f:
        folder_path="output/static/img"
        img_names = os.listdir(folder_path)
        text=f.read()
        subtext(text,num)
        download(text,img_names)

if __name__=='__main__':      
    spiderALL()
    #spiderSingle(1)