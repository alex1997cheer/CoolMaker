import io
import selenium
import Picture 
import JXml
import Vedio
from selenium import webdriver
from time import sleep
from PIL import Image



class Article:
 url = ('https://www.youtube.com/watch?v=E22DvRW3Few')
 def GotoUrl(self,url):
    USERNAME = "Administrator"
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized') 
    # options.add_argument('--headless')    
    options.add_argument("--user-data-dir=" + f"C:/Users/{USERNAME}/AppData/Local/Google/Chrome/User Data/")
    driver = webdriver.Chrome(executable_path ="F:\Project\CoolMaker\Driver\chromedriver.exe",options = options)
    driver.get(url)
    return driver

 def GetHotComment(self,driver):
    sleep(3)
    #删除搜索框
    driver.execute_script("document.getElementById('container').remove()")    
    #删除右侧视频推荐
    driver.execute_script("document.getElementById('secondary').remove()")    
    sleep(3)
    driver.execute_script("var q=document.documentElement.scrollTop=700")
    hotmComment =  set()
    count = 0
    step = 0
    while  len(hotmComment) < 40:
        sleep(1)
        elements = driver.find_elements_by_xpath("//div[@id='contents']/ytd-comment-thread-renderer")
        if  count > 5:             
            driver.refresh()
            hotmComment =  set()
            sleep(3)
            driver.execute_script("document.getElementById('container').remove()")    
            count = 0 
            step = 0   
        elif len(elements) <= 0 or len(elements) == len(hotmComment):
            sleep(1)
            count += 1
            step += 1000
            driver.execute_script("var q=document.documentElement.scrollTop={}".format(step))
        else:
            for item in elements:
                # print("爬取:{}".format(item.text))
                # print('-----------------------------')
                hotmComment.add(item)      
                count = 0    

    return hotmComment

 def ElementScreenShot(self,driver,elements,savePath):
     for index, element in enumerate(elements):         
         driver.execute_script("""
                                   arguments[0].style.width='1813px';
                                   arguments[0].style.height='918px';
                               """,element)
         element.screenshot(savePath+"\image{0}{1}".format(index,".png"))          

'''
 driver = GotoUrl(url)
 elements = GetHotComment(driver)
 ElementScreenShot(driver,elements)
 xml = JXml.GenerateXML(elements)
 Picture.checkEmptyPicture(xml)
 Vedio.writeVedioList("Images/list.txt",'result.xml')
 Vedio.combineVedio()
 '''




