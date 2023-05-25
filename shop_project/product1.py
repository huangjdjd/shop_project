from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3 as sql
import json as js
app=Flask(__name__)
app.secret_key = "b22VD7bKVsEa"
i=0
@app.route('/')
def main():
    return render_template('project1.html')
@app.route('/<msg>')
def mainf(msg):
    return render_template("project1.html",msg=msg)
@app.route('/mainsign')
def mainsign():
    if i==0:
        return redirect(url_for('main'))
    else:
        return render_template("project1.html",msg="log")
@app.route('/product1', methods=['post','get'])
def product1():
    return render_template('product.html')
@app.route('/product1/<msg>', methods=['post','get'])
def product1f(msg):
    return render_template('product.html',msg=msg)
@app.route('/product2/<msg>', methods=['post','get'])
def product2f(msg):
    return render_template('product2.html',msg=msg)
@app.route('/product2',methods=['post','get'])
def product2():
    return render_template('product2.html')
@app.route('/sign')
def sign():
    return render_template('signin.html')
@app.route('/sign/<msg>')
def signf(msg):
    return render_template('signin.html',msg=msg)
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/register/<msg>')
def registerf(msg):
    return render_template('register.html',msg=msg)
@app.route('/shopcart')
def shopcart():
    return render_template('shopchart.html')
@app.route('/shopcart/<msg>')
def shopcartf(msg):
    return render_template('shopchart.html',msg=msg)
@app.route('/sign_action',methods=['post','get'])
def sign_action():
    global i
    if request.method == "POST":
        account=request.form.get('account')
        password=request.form.get('password')
    con=sql.connect('user.db')
    cur=con.cursor()

    if account and password:
        cur.execute('select account from userlist where account='+account)
        list2=cur.fetchone()
        if list2:
            cur.execute('select password from userlist where account='+account)
            judge=cur.fetchone()
            print(judge)
            if password==judge[0]:
                session['user']=account
                i+=1
                return_msg="login out"
                return redirect(url_for('mainf',msg=return_msg))
            else:
                return_msg="請輸入正確密碼"
                return redirect(url_for('signf',msg=return_msg))
        else:
            return_msg="請輸入正確帳號"
            return redirect(url_for('signf',msg=return_msg))
    else:
        return_msg="請輸入帳號密碼"
        return redirect(url_for('signf',msg=return_msg))

@app.route('/register_action',methods=['post','get'])
def register_action():
    con=sql.connect('user.db')
    cur=con.cursor()
    if request.method == "POST":
        email=request.form.get('email')
        account=request.form.get('account')
        password=request.form.get('password')
        surepass=request.form.get('surepass')
    if email and account and password and surepass:
        if "@gmail.com" in email:
            if " " in password:
                return_msg="密碼不能含空白"
                return redirect(url_for('registerf',msg=return_msg))
            else:
                if password != surepass:
                    return_msg="密碼必須相同"
                    return redirect(url_for('registerf',msg=return_msg))
                else:
                    
                    cur.execute(f"Insert into userlist (account,password,email) values('{account}','{password}','{email}')")
                    con.commit()
                    print('a')
                    return redirect(url_for('sign'))
        else:
            return_msg="email必須使用gmail格式"
            return redirect(url_for('registerf',msg=return_msg))

    else:
        return_msg="請每項都要輸入"
        return redirect(url_for('registerf',msg=return_msg))
@app.route('/shop_action',methods=['post','get'])
def shop_action():
    # print(i)
    global i
    if i:
        list2=[]
        id=session['user']
        con=sql.connect('user.db')
        cur=con.cursor()
        # receive=request.get_data().decode("utf-8")
        receive=js.loads(request.data)
        print(receive)
        cur.execute('select userid from shoplist where userid='+id)
        judgenum=cur.fetchone()
        if judgenum:
            cur.execute("select shopname from shoplist where userid="+id)
            judgename=list(cur.fetchall())
            print(judgename)
            for i in judgename:
                for j in i:
                    if j==receive[0]: 
                        list2.append(j)  
                # cur.execute('select shohpnumber from shoplist where  user
            if receive[0] in list2:
                cur.execute("UPDATE shoplist SET shopnumber = ? WHERE userid = ? AND shopname = ?", (receive[1], id, receive[0]))
                con.commit()
                return "購買成功"
            else:
                cur.execute(f"Insert into shoplist(shopname,shopnumber,userid) values('{receive[0]}','{receive[1]}','{id}') ")
                con.commit()
                return "購買成功"
        else:
            cur.execute(f"Insert into shoplist(shopname,shopnumber,userid) values('{receive[0]}','{receive[1]}','{id}') ")
            con.commit()
            return "購買成功"
    else:
        return "請登入再購買"
@app.route('/showcart',methods=['post','get'])
def showcart():
    if i :

        cart=[]
        id=session['user']
        con=sql.connect('user.db')
        cur=con.cursor()
        cur.execute("select userid,shopname,shopnumber from shoplist where userid="+id)
        shop=cur.fetchall()
        cart.append(shop)
        # cart=js.dumps(cart)

        return render_template('shopchart.html',msg=shop)
    else:
        la={}
        print("i")
        return render_template('shopchart.html',msg=la)
@app.route('/sum',methods=['post','get'])
def sum():
    global i
    if i:
        id=session['user']
        con=sql.connect('user.db')
        cur=con.cursor()
        cur.execute("select shopname from shoplist where userid="+id)
        owner=cur.fetchall()
        cur.execute("Select allshopname from allshopnumber")
        shop=cur.fetchall()
        print(shop)
        print(owner)
        for i in shop:
            for j in owner:
                if j==i:
                    print(j[0])
                    cur.execute(f"SELECT shopnumber FROM shoplist WHERE userid={id} AND shopname='{j[0]}'")

                    num=cur.fetchone()
                    print(num)
                    cur.execute(f"select allshopnum from allshopnumber where allshopname='{j[0]}'")
                    shop_num=cur.fetchone()
                    print(shop_num)
                    sum=int(shop_num[0])-int(num[0])
                    cur.execute(f"Update allshopnumber set allshopnum={sum} where allshopname='{j[0]}'")
                    con.commit()
        cur.execute('delete from shoplist where userid='+id)
        con.commit()
        print("I")
        return redirect(url_for('mainsign',msg="log"))
    else:
        return_msg="請登入再購買"
        return redirect(url_for('main'))
@app.route("/judgesum",methods=['post','get'])
def judgesum():
    sumlist=js.loads(request.data)
    con=sql.connect('user.db')
    cur=con.cursor()
    cur.execute(f"Select allshopnum from allshopnumber where allshopname='{sumlist[0]}'")
    sure_goods=cur.fetchone()
    print(sure_goods[0])
    print(sumlist[1])
    if int(sumlist[1])>sure_goods[0]:
        print("i")
        return "超出範圍"
    else:
        return "購買成功"
@app.route('/earn',methods=['post','get'])
def earn():
    money=js.loads(request.data)
    con=sql.connect('user.db')
    cur=con.cursor()
    id=session['user']
    cur.execute(f"Insert into earnmoney (userid,money) values('{id}','{money}')")
    con.commit()
    return "ok"
@app.route('/game',methods=['post','get'])
def game():
    con=sql.connect('user.db')
    cur=con.cursor()
    score=js.loads(request.data)
    if i and i!=0:
        id=session['user']
        cur.execute(f"Insert into shoplist (shopname,shopnumber,userid) values('智慧','1','{id}')")
        con.commit()
        return "成功獲得"
    else:
        print("i")
        return "請登入再玩才能獲得"
@app.route('/logout')
def logout():
    global i
    con=sql.connect('user.db')
    cur=con.cursor()
    i=0
    session.pop('user')
    return redirect(url_for('main'))
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

