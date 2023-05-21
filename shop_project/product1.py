from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3 as sql
import json as js
app=Flask(__name__)
app.secret_key = "b22VD7bKVsEa"
@app.route('/')
def main():
    return render_template('project1.html')
@app.route('/<msg>')
def mainf(msg):
    return render_template("project1.html",msg=msg)
@app.route('/product1', methods=['post','get'])
def product1():
    return render_template('product.html')
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
@app.route('/sign_action',methods=['post','get'])
def sign_action():
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

@app.route('/logout')
def logout():
    
    session.pop('user')
    return redirect(url_for('main'))
if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")

