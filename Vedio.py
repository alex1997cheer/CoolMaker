import lxml
from lxml import etree
import os




def writeVedioList(txtUrl,xmlUrl):
    fo = open(txtUrl, "r+")
    print ("文件名: ", fo.name)
    root = etree.parse(xmlUrl)
    cuts = root.xpath("//cut")
    fo = open(txtUrl, "r+")
    for index, cut in enumerate(cuts):
        img = cut.find('img').text
        out = r'F:\\Project\\CoolMaker\\Images\\out{}.avi'.format(index)
        os.system("ffmpeg -f image2 -loop 1  -i {} -t 5 -b 5000k -vcodec libx264   -y {}".format(img,out))
        print ("文件名: ", out)
        str = r"file {}".format(out)
        fo.seek(0, 2)
        line = fo.write( str +'\r' )
    fo.close()


def combineVedio():
    os.system('ffmpeg -y -f concat -safe 0 -i Images/list.txt -b 5000k -vcodec libx264 -c copy Images/app.avi')
    # 添加白色背景
    os.system('ffmpeg -y -f lavfi -i color=c=white:s=1920x1080 -i Images/app.avi -b 5000k -vcodec libx264 -filter_complex overlay=x=58:79 -t 190 Images/app2.avi')
    # 添加gig
    os.system('ffmpeg -y -i Images/app2.avi -ignore_loop 0  -i Images/longmao.gif -b 5000k -vcodec libx264 -filter_complex overlay=x=1300:500 -t 190 Images/app3.avi')
    # 添加背景音乐
    os.system('ffmpeg -y -i Images/app3.avi  -i Images/bgm2.mp3 -b 5000k -vcodec libx264 -t 190 Images/app4.avi')


# combineVedio()
#writeVedioList("Images/list.txt",'result.xml')



