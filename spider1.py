#-*- coding = utf-8 -*-
#time 2020 5.29

from bs4 import BeautifulSoup
import re
import xlwt
import sqlite3
import urllib.request,urllib.error




def main():
    baseurl = "https://movie.douban.com/top250?start="
    for i in range(1,10):
        speurl = baseurl + str(i*25)

        htmlpage = askURL(baseurl)
#    print(type(htmlpage))
        tdata = getData(htmlpage)
        saveDatasql(tdata,"./move520.db")
    print("work Done!")
findLink = re.compile(r'<a href="(.*)">')
findImg = re.compile(r'<img.*src="(.*?)"',re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findTating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*?)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>',re.S) #someThing about movie


def getData(pageStr):
    datalist = []
    soup = BeautifulSoup(pageStr,"html.parser")

    for item in soup.find_all('div',class_="item"):
        item = str(item)
        data =[]
        link = re.findall(findLink,item)[0]
        data.append(link)

        imgSrc = re.findall(findImg,item)[0]
        data.append(imgSrc)
        
        titles = re.findall(findTitle,item)
        if(len(titles) == 2):
            data.append(titles[0])
            data.append(titles[1].replace("/",""))
        else:
            data.append(titles[0])
            data.append("   ")

        rating = re.findall(findTating,item)[0]
        data.append(rating)

        judgeNum = re.findall(findJudge,item)
        if(len(judgeNum) >0):

            data.append(judgeNum[0])
        else:
            data.append("no one judge")
    
        inq = re.findall(findInq,item)
        if(len(inq) !=0 ):
            data.append(inq[0])
        else:
            data.append("   ")

        bd = re.findall(findBd,item)[0]
        bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
        data.append(bd.strip())

        datalist.append(data)
        
      #  print(link

    return datalist

def askURL(url):
    head = {
            "User-Agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 "
            }
    request = urllib.request.Request(url,headers=head)
    html =""
    responese = urllib.request.urlopen(request)
    html = responese.read().decode("utf-8")
    #print(html)
    return html

def saveData(content,savePath):
    print("saveing...")
    xlsbook = xlwt.Workbook(encoding = "utf-8")
    xlssheet = xlsbook.add_sheet("dou ban movies")
    for i in range(25):
        for j in range(8):
            xlssheet.write(i,j,content[i][j])

    xlsbook.save("douban.xls")

def saveDatasql(content,savePath):
    print("saving to sql")
    sql = '''
        create  table if not exists movie250
        (
          id integer primary key autoincrement,
          info_link text,
          pic_link text,
          cname varchar,
          ename varchar,
          score numeric,
          rated numeric,
          intruduce text,
          info text
          )

    '''
    conn = sqlite3.connect(savePath)
    cursor = conn.cursor()
    cursor.execute(sql)
    print("database init done")

    for data in content:
        for index in range(len(data)):
            if index == 5 or index ==4:
                continue
            data[index] = '"'+str(data[index]) + '"'

        sql2 = '''
            insert into movie250 ( info_link,pic_link,cname,ename,score,rated,intruduce,info) values(%s)
        '''%",".join(data)

        cursor.execute(sql2)
    

    conn.commit()
    cursor.close()

    conn.close()
    print(" save to sql done")
if __name__ == "__main__":
    main()
