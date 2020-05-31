import sqlite3

conn = sqlite3.connect("move520.db")

cor = conn.cursor()
sql = "select * from movie250"

data  = cor.execute(sql)
datalist = []
for item in data:
    print(item)
    print("\n")
    print(item[1])
print(data )

cor.close()
conn.close()
