import sqlite3

dbPath = 'WeChat.db'

def ChengYuSelectLike(name):
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql="SELECT * FROM ChengYu WHERE ChengYu Like '%{0}%'".format(name)
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            value.append(row[1])
        conn.close()
        return value
    except:
        return None

def ChengYuSelectEqual(name):
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql="SELECT * FROM ChengYu WHERE ChengYu='{0}'".format(name)
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            value.append(row[1])
        conn.close()
        return value
    except:
        return None

def NaojjzwSelect():
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql="SELECT * FROM guess"
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            t=[]
            t.append(row[1])
            t.append(row[2])
            value.append(t)
        conn.close()
        return value
    except:
        return None

def ZimiSelect(id):
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql="SELECT * FROM tb_zimi where id={0}".format(id)
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            value.append(row[1])
            value.append(row[2])
        conn.close()
        return value
    except:
        return None

def ZimiInsert(miyu,daan):
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute("INSERT INTO tb_zimi (miyu,daan) VALUES('{0}','{1}')".format(miyu,daan))
    conn.commit()
    conn.close()

def YizhandaodiSelect(id):
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql="SELECT * FROM tb_yizhandaodi WHERE id={0}".format(id)
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            value.append(row[1])
            value.append(row[2])
        conn.close()
        return value
    except:
        return None
