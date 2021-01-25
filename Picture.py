import os
import selenium
from selenium import webdriver
from PIL import Image
import lxml
from lxml import etree

def checkEmptyPicture(url):
    xml = etree.parse(url)
    cuts = xml.xpath("//cut")
    matrix  = [[10, 10], [10, 20], [10, 30],[10, 40],[10, 50],[20, 10], [20, 20], [20, 30],[20, 40],[20, 50],[30, 10], [30, 20], [30, 30],[30, 40],[30, 50]]

    for cut in cuts:
        ImageUrl = cut.find("img").text
        img = Image.open(ImageUrl)
        img = img.convert("RGBA")
        pixdata = img.load()
        empty = True
        for local in matrix:
            pixel = pixdata[local[0], local[1]]
            if pixel[0] != 249 and pixel[1] != 249 and pixel[2] != 249:
                empty = False    
        if empty:
            print(ImageUrl)
            cut.getparent().remove(cut) 
            os.remove(ImageUrl)  
    xml.write(url, encoding = 'utf-8')   
        
   

def scan_files(directory,prefix=None,postfix=None):
    files_list=[]    
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root,special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root,special_file))
            else:
                files_list.append(os.path.join(root,special_file))                          
    return files_list


# checkEmptyPicture("result.xml")