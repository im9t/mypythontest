import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import sqlite3
import os
from os import path

d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
font_path = d + '/fonts/SourceHanSerif/SourceHanSerifK-Light.otf'

filename = 'p1.jpg'
con = sqlite3.connect('move520.db')
cur = con.cursor()
sql = 'select intruduce from movie250'

data = cur.execute(sql)
text  =""
for item in data:
    text  += item[0]
    
cut = jieba.cut(text)
string = " ".join(cut)

img = Image.open(filename)
img_array = np.array(img)
wc = WordCloud(font_path='./wqy-zenhei.ttc',background_color='white',mask=img_array)
wc.generate_from_text(string)

fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
plt.savefig('newWordCloud.jpg',dip = 500)
