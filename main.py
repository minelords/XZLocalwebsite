from source import get_topic,begin
from spider import download,spiderALL,spiderSingle




#获取主页面源码，第一次必须执行
#get_topic()


#获取文章源码
#pages=[1,2,3]  #自行选择页数
#begin(pages)


#生成已获取的页面
#spiderALL() #默认会下载图片

#如果不下载图片请使用：
#spiderALL(False)

#生成单个文章页面
#选择生成的文章标识，例如'https://xz.aliyun.com/t/14645'
#num=14645   
#spiderSingle()