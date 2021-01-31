#from xml.etree import ElementTree as  etree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree
import selenium
from selenium import webdriver
from xml.dom import minidom
import lxml
from lxml import etree


def prettyXml(element, indent, newline, level = 0): 
    # 判断element是否有子元素
    if element:
        # 如果element的text没有内容      
        if element.text == None or element.text.isspace():     
            element.text = newline + indent * (level + 1)      
        else:    
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)    
    # 此处两行如果把注释去掉，Element的text也会另起一行 
    #else:     
        #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level    
    temp = list(element) # 将elemnt转成list    
    for subelement in temp:    
        # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
        if temp.index(subelement) < (len(temp) - 1):     
            subelement.tail = newline + indent * (level + 1)    
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个    
            subelement.tail = newline + indent * level   
        # 对子元素进行递归操作 
        prettyXml(subelement, indent, newline, level = level + 1)     

def GenerateXML(elements,savePath,xmlSavePath):
    # generate root node
    root = Element('vedio')
    for index,element in enumerate(elements):
        cut = SubElement(root, 'cut')
        cut.attrib['order'] = str(index)
        time = SubElement(cut,'time')
        time.text = '2'
        img = SubElement(cut,'img')
        img.text = savePath+'\image{}.png'.format(index)
        author = SubElement(cut,'author')
        author.text =  element.find_element_by_tag_name("span").text
        content = SubElement(cut,'content')
        content.text = element.find_element_by_id("content-text").text
        like = SubElement(cut,'like')
        like.text = element.find_element_by_id("vote-count-middle").text
    tree = ElementTree(root)
    # write out xml data
    tree.write(xmlSavePath, encoding = 'utf-8')
    prettyXml(tree.getroot(),'\t', '\n')
    tree.write(xmlSavePath, encoding = 'utf-8')
    return xmlSavePath

# doc = etree.parse('result.xml')
# cuts = doc.xpath("cut")
# for item in cuts:
#     time = item.find("time").text
#     img = item.find("img").text
#     auther = item.find("auther").text
#     content = item.find("content").text
#     tlikeime = item.find("like").text
#     dislike = item.find("dislike").text

#     print(item)


