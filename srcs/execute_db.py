import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()
db = os.getenv('db')

def create_db():
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute("DROP TABLE stocks")
    cur.execute('CREATE TABLE stocks(name STRING,amount INTEGER,sales REAL)')

    # データベースへコミット。これで変更が反映される。
    conn.commit()
    conn.close()
def create_table():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('CREATE TABLE stocks(name STRING,amount INTEGER,sales INTEGER)')
    conn.commit()
    conn.close()
def delete_table():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("DROP TABLE stocks")
    conn.commit()
    conn.close()

def update(name,amount = 1):
    global db
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT * FROM stocks WHERE name = ?',[name])
    if len(cur.fetchall())==0:
        cur.execute('INSERT INTO stocks(name,amount,sales) values(?,?,0)',[name,amount])
    else:
        cur.execute('UPDATE stocks SET amount = amount + ? WHERE name = ?',[amount,name])
    conn.commit()
    conn.close()

def check(name = None):
    global db
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    resp = {}
    if name == None:
        cur.execute('SELECT name,amount FROM stocks')
        for data in cur.fetchall():
            if data[1] > 0:
                resp[str(data[0])] = int(data[1])
    else:
        cur.execute('SELECT name,amount FROM stocks WHERE name = ?',[name])
        data = cur.fetchone()
        if data != None:
            resp[name] = int(data[1])
        else:
            resp = {"message":"ERROR"}
    conn.commit()
    conn.close()
    return resp

def sales(name,amount = 1, price = None):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT amount FROM stocks WHERE name = ?',[name])
    data = cur.fetchone()
    if data != None:
        data_amount = data[0]
        if amount > data_amount:
            amount = data_amount
        if price is None:
            cur.execute('UPDATE stocks SET amount = amount - ? WHERE name = ?',[amount,name])
        else:
            cur.execute('UPDATE stocks SET amount = amount - ?, sales = sales + ? WHERE name = ?',[amount,(amount*price),name])

    else:
        return {"message":"ERROR"}

    conn.commit()
    conn.close()

def getsales():
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT sales FROM stocks')
    sales = 0
    for data in cur.fetchall():
        sales += data[0]
    conn.commit()
    conn.close()
    resp = float(sales)
    if float('{:.2f}'.format(resp)) < resp:
        resp = float('{:.2f}'.format(resp+0.01)) 
    else:
        resp = float('{:.2f}'.format(resp))
    return {"sales":resp}

# 全削除
def all_delete():
    global db
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('DELETE FROM stocks')
    conn.commit()
    conn.close()