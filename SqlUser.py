import sqlite3

dbPath = 'WeChat.db'


def UserInsert(name,qun):#根据姓名查询
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    c.execute("INSERT INTO tb_User (name,qun) VALUES('{0}','{1}')".format(name,qun))
    conn.commit()
    conn.close()

def UserSelectAll():
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql="SELECT * from tb_User"
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            t=[]
            t.append(row[0])
            t.append(row[1])
            t.append(row[2])
            t.append(row[3])
            t.append(row[4])
            t.append(row[5])
            t.append(row[6])
            t.append(row[7])
            t.append(row[8])
            value.append(t)
        conn.close()
        return value
    except:
        return None

def UserSelect(name,qun=""):
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        if qun=="":
            sql="SELECT * from tb_User WHERE name like '%{0}%'".format(name)
        else:
            sql="SELECT * from tb_User WHERE name like '%{0}%' and qun='{1}'".format(name,qun)
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            value.append(row[0])
            value.append(row[1])
            value.append(row[2])
            value.append(row[3])
            value.append(row[4])
            value.append(row[5])
            value.append(row[6])
            value.append(row[7])
            value.append(row[8])
        conn.close()
        return value
    except:
        return None

def UserSelect1(id):#根据ID查询信息
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        cursor = c.execute("SELECT * from tb_User WHERE id='{0}'".format(id))
        value = []
        for row in cursor:
            value.append(row[0])
            value.append(row[1])
            value.append(row[2])
            value.append(row[3])
            value.append(row[4])
            value.append(row[5])
            value.append(row[6])
        conn.close()
        return value
    except:
        return None

def UserSelect2(boss):#查询奴隶
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        cursor = c.execute("SELECT * from tb_User WHERE boss='{0}'".format(boss))
        value = []
        for row in cursor:
            t=[]
            t.append(row[0])
            t.append(row[1])
            t.append(row[2])
            t.append(row[3])
            t.append(row[4])
            t.append(row[5])
            t.append(row[6])
            value.append(t)
        conn.close()
        return value
    except:
        return None

def UserUpdateBalance(name,op):
    try:
        conn=sqlite3.connect(dbPath)
        c=conn.cursor()
        cursor=c.execute("SELECT * from tb_User WHERE name='{0}'".format(name))
        for row in cursor:
            gold= row[2]
        gold=gold+op;
        if gold<0:
            return "余额不足"
        c.execute("UPDATE tb_User SET balance={0} WHERE name='{1}'".format(gold,name))
        conn.commit()
        conn.close()
    except:
        pass

def UserUpdateBoss(boss,name):
    try:
        conn=sqlite3.connect(dbPath)
        c=conn.cursor()
        c.execute("UPDATE tb_User SET boss={0} WHERE name='{1}'".format(boss,name))
        conn.commit()
        conn.close()
    except:
        pass

def UserUpdateMoney(money,name):
    try:
        conn=sqlite3.connect(dbPath)
        c=conn.cursor()
        c.execute("UPDATE tb_User SET money={0} WHERE name='{1}'".format(money,name))
        conn.commit()
        conn.close()
    except:
        pass


def UserUpdateWork(name,time,work):
    try:
        conn=sqlite3.connect(dbPath)
        c=conn.cursor()
        c.execute("UPDATE tb_User SET worktime='{0}',work='{1}' WHERE name='{2}'".format(time,work,name))
        conn.commit()
        conn.close()
    except:
        pass

def UserUpdateFlag(name,flag):
    try:
        conn=sqlite3.connect(dbPath)
        c=conn.cursor()
        c.execute("UPDATE tb_User SET flag='{0}' WHERE name='{1}'".format(flag,name))
        conn.commit()
        conn.close()
    except:
        pass

def UserSelectPaiHang(qun,type):
    try:
        conn = sqlite3.connect(dbPath)
        c = conn.cursor()
        sql="SELECT * FROM tb_User WHERE qun='{0}' ORDER BY {1} DESC".format(qun,type)
        cursor = c.execute(sql)
        value = []
        for row in cursor:
            t=[]
            t.append(row[0])
            t.append(row[1])
            t.append(row[2])
            t.append(row[3])
            t.append(row[4])
            t.append(row[5])
            t.append(row[6])
            t.append(row[7])
            t.append(row[8])
            value.append(t)
        conn.close()
        return value
    except:
        return None
