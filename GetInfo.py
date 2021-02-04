import io
import os
from pathlib import Path
import selenium
import Picture 
import JXml
import Vedio
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Article import Article
from hashlib import md5
class GetInfo:
    def __init__(self,searchKey,chromeDriverPath,grabNumber):
        self.SearchKey=searchKey   #搜索关键字
        self.ChromeDriverPath=chromeDriverPath   #驱动路径
        self.GrabNumber=grabNumber #抓取个数
    
    #开始获取页面内容
    def startGet(self):
        print('启动列表数据爬取')
        USERNAME = "Administrator"
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized') 
        # options.add_argument('--headless')    
        options.add_argument("--user-data-dir=" + f"C:/Users/{USERNAME}/AppData/Local/Google/Chrome/User Data/")
        driver = webdriver.Chrome(executable_path=self.ChromeDriverPath,options=options)
        url=('https://www.youtube.com/results?search_query='+self.SearchKey+'&sp=CAM%253D')
        driver.get(url)
        time.sleep(5)
        #self.scroll(driver)
        #eleList=driver.find_elements_by_xpath('//*[@id="contents"]/ytd-video-renderer')
        #print(len(eleList))
        urlList=set()
        count = 0
        step = 0
        beforeLen=0 
        maxRetryCount=10 #最大重爬次数 
        retryCount=0 #重爬次数
        while len(urlList) < self.GrabNumber:
            eleList=driver.find_elements_by_xpath('//*[@id="contents"]/ytd-video-renderer')
            for row in eleList:
                href=row.find_element_by_id('video-title').get_attribute('href')
                if len(urlList)<self.GrabNumber:
                    urlList.add(href)
            if len(urlList)<=beforeLen:
                if retryCount < maxRetryCount:
                    print('此次没有更新数据，尝试重新爬取')
                    retryCount+=1
                else:
                    print('重爬达到上限，关闭爬取')
                    retryCount=0    
                    break
            beforeLen=len(urlList)
            count += 1
            step += 1000 
            driver.execute_script("var q=document.documentElement.scrollTop={}".format(step))
        driver.close()
        print('列表数据爬取完毕,准备进入详情页')
        time.sleep(5)
        article= Article()
        for url in iter(urlList):
            print('爬取详情页面在:'+url)
            driver = article.GotoUrl(url)
            elements = article.GetHotComment(driver)
            path=self.createImageSavePath(url)
            article.ElementScreenShot(driver,elements,path)
            print('生成xml')
            xmlPath=self.createXmlSavePath(url)
            xml = JXml.GenerateXML(elements,path,xmlPath)
            print('生成xml结束')
            Picture.checkEmptyPicture(xml)
            Vedio.writeVedioList("Images/list.txt",xmlPath,path)
            Vedio.combineVedio(path)
            driver.close()
            print(url+'爬取完毕,准备进入下一条')
           # Vedio.writeVedioList("Images/list.txt",'result.xml')
           # Vedio.combineVedio()
        print('全部爬取完毕')
    #生成截图存储路径
    def createImageSavePath(self,url):
        md5Name=md5(url.encode('utf8')).hexdigest()
        savePath =f"F:/Project/CoolMaker/Images/{md5Name}" 
        dir = Path(savePath)
        if not dir.is_dir():
            os.mkdir(savePath)
        return savePath
     #生成xml存储路径
    def createXmlSavePath(self,url):
        md5Name=md5(url.encode('utf8')).hexdigest()
        savePath =f"F:/Project/CoolMaker/Xml/{md5Name}.xml" 
        file = Path(savePath)
        '''
        if not file.is_file:
            os.mknod(savePath)
        '''
        return savePath
    #根据路径进入详情页获取信息
    def getInfoMessage(self,url):
        print(url)
        USERNAME = "Administrator"
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized') 
        #options.add_argument('--headless')    
        options.add_argument("--user-data-dir=" + f"C:/Users/{USERNAME}/AppData/Local/Google/Chrome/User Data/")
        driver = webdriver.Chrome(executable_path=self.ChromeDriverPath,options=options)
        url=(url)
        driver.get(url)
        time.sleep(8)
        #获取标题
        infoEle=driver.find_element_by_id('info')
        titleEle=infoEle.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
        #title=titleEle.get_attribute('innerHTML')
        title=titleEle.text
        #获取评论内容
        '''
        contentsEle=driver.find_element_by_id('contents')
        commentList= driver.find_elements_by_xpath('//*[@id="contents"]/ytd-comment-thread-renderer')
        print(contentsEle.get_attribute('innerHTML'))
        '''
        time.sleep(50)
        driver.close()
        return True

getInfo=GetInfo('中国 抖音','F:\Project\CoolMaker\Driver\chromedriver.exe',50)
getInfo.startGet()