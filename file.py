import io
import lxml
from lxml import etree
# 打开文件

def writeVedioList(filePath,txtUrl):
    fo = open(txtUrl, "r+")
    print ("文件名: ", fo.name)

    root = etree.parse(xmlUrl)
    cuts = root.xpath("//cut")
    img = filePath
    str = "file {}".format(img)
    # 在文件末尾写入一行
    fo.seek(0, 2)
    line = fo.write( str +'\r' )
    # 关闭文件
    fo.close()

writeVedioList("Images/list.txt",'result.xml')
