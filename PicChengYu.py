# coding=utf-8
import random
from urllib import parse,request
import requests
from bs4 import BeautifulSoup
from PIL import Image



class PicChengyu:


    main='http://www.hydcd.com/cy/fkccy/'
    index=['index.htm','index2.htm','index3.htm','index4.htm','index5.htm','index6.htm','index7.htm','index8.htm','index9.htm','index10.htm']

    def GetPicAndCY(self):
        try:
            url=self.main+self.index[random.randint(0,len(self.index)-1)]
            response=request.urlopen(url)
            data=response.read().decode('gbk')
            soup=BeautifulSoup(data,'html.parser')
            tds=soup.find_all('td')
            value=[]
            for i in tds:
                t=[]
                isoup=BeautifulSoup(str(i),'html.parser')
                ps=isoup.find_all('p')
                if len(ps)!=3:
                    continue
                img=isoup.find_all('img')
                if len(img)<=0:
                    continue
                imgsrc=img[0]['src']
                imgsrc=self.main+imgsrc
                a=isoup.find_all('a')
                if len(a)<=0:
                    continue
                answer=a[0].string
                t.append(imgsrc)
                t.append(answer)
                value.append(t)
            return value
        except:
            return None


    def DownLoadPic(self,url):
        try:
            imgFile=requests.get(url).content
            imgType=url[len(url)-3:len(url)]
            with open('caichengyu.'+imgType,'wb') as img:
                img.write(imgFile)
                img.close()
            try:
                im = Image.open('caichengyu.png')
                bg = Image.new("RGB", im.size, (255,255,255))
                bg.paste(im,im)
                bg.save('caichengyu.jpg')
            except:
                pass
            return True
        except:
            return False

