from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
import sqlite3

def getText(sqlPath):
    conn = sqlite3.connect(sqlPath)
    cur = conn.cursor()
    
    sql = 'select intruduce from movie250'

    data = cur.execute(sql)
    text =" " 

    for item in data:
        text += item[0]

    cut = jieba.cut(text)
    string = "  ".join(cut)

    print("There are %d words"%len(string))
    return string

def generatePic(text):
    wc = WordCloud(font_path ='./wqy-zenhei.ttc',background_color = None,width = 1024,height = 768,mode='RGBA' ,max_words=9000,collocations=False).generate(text)
    plt.imshow(wc,interpolation = 'bilinear')
    plt.axis('off')
    plt.show()

   # wc.to_file('wordcloudpure.png')
    plt.savefig('wordcloudptl.png',dpi=800) 
generatePic(getText('move520.db'))
