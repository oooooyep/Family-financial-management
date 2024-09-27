from flask import Flask, render_template, session
from flask import request, url_for, redirect, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)
app.secret_key = '666'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hhhhh4221.'
app.config['MYSQL_DB'] = '记账系统'


mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # 检查帐户是否存在MySQL中
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user_name = %s AND password = %s', (username, password))
        # 获取一条记录并返回结果
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['role_id'] = account['role_id']
            session['true_name'] = account['true_name']
            if session['role_id'] == 1:
                return redirect(url_for('home'))
            elif session['role_id'] == 2:
                return redirect(url_for('home1'))
    return render_template('登录.html')


# 管理员主界面
@app.route('/home')
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT u.user_name, SUM(d.amount) AS total_expense '
                   'FROM user u '
                   'JOIN details d ON u.user_id = d.user_id '
                   'GROUP BY u.user_name '
                   'ORDER BY total_expense DESC')
    income = cursor.fetchall()
    cursor.execute('SELECT (SELECT SUM(money) FROM salary) AS total_income')
    total_income = cursor.fetchall()
    cursor.execute('SELECT  (SELECT SUM(amount) FROM details)  AS total_expense')
    total_expense = cursor.fetchall()
    cursor.execute('SELECT u.user_name, SUM(d.amount) AS total_expense '
                   'FROM user u '
                   'JOIN details d ON u.user_id = d.user_id '
                   'GROUP BY u.user_name '
                   'ORDER BY total_expense DESC')
    expenditure = cursor.fetchall()
    return render_template('主要.html',
                           user=session, income=income,
                           total_income=total_income, total_expense=total_expense,
                           expenditure=expenditure)


# 家庭成员主界面
@app.route('/home1')
def home1():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT u.user_name, SUM(d.amount) AS total_expense '
                   'FROM user u '
                   'JOIN details d ON u.user_id = d.user_id '
                   'GROUP BY u.user_name '
                   'ORDER BY total_expense DESC')
    income = cursor.fetchall()
    cursor.execute('SELECT (SELECT SUM(money) FROM salary) AS total_income')
    total_income = cursor.fetchall()
    cursor.execute('SELECT  (SELECT SUM(amount) FROM details)  AS total_expense')
    total_expense = cursor.fetchall()
    cursor.execute('SELECT u.user_name, SUM(d.amount) AS total_expense '
                   'FROM user u '
                   'JOIN details d ON u.user_id = d.user_id '
                   'GROUP BY u.user_name '
                   'ORDER BY total_expense DESC')
    expenditure = cursor.fetchall()
    return render_template('主要1.html',
                           user=session, income=income,
                           total_income=total_income, total_expense=total_expense,
                           expenditure=expenditure)


# 用户系统
@app.route('/user_manage')
def user_manage():
    if 'loggedin' in session:
        page = int(request.args.get('page', 1))
        per_page = 5
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(*) FROM user"
        cursor.execute(query)
        total = cursor.fetchone()['COUNT(*)']
        start = (page-1)*per_page
        end = start + per_page
        query = "SELECT * FROM user  "
        cursor.execute(query)
        all_users = cursor.fetchall()
        all_users_list = list(all_users)
        users = all_users_list[start:end]
        pagination = Pagination(all_users, page=page, per_page=per_page, total=total, items=all_users[page - 1])
        context = {
            'pagination': pagination,
            'users': users
        }
        return render_template('用户管理.html', **context, user=session)
    return render_template('用户管理.html', paginate=6,  user=session)


# 支出管理
@app.route('/pay_manage')
def pay_manage():
    if 'loggedin' in session:
        page = int(request.args.get('page', 1))
        per_page = 5
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(*) FROM details_type"
        cursor.execute(query)
        total = cursor.fetchone()['COUNT(*)']
        start = (page-1)*per_page
        end = start + per_page
        query = "SELECT * FROM  details_type "
        cursor.execute(query)
        all_details_type = cursor.fetchall()
        all_details_type_list = list(all_details_type)
        details_type = all_details_type_list[start:end]
        pagination = Pagination(details_type, page=page, per_page=per_page, total=total, items=all_details_type[page - 1])
        context = {
            'pagination': pagination,
            'details_type': details_type
        }
        return render_template('支出管理.html', **context,  user=session)
    return render_template('支出管理.html', paginate=6, user=session)


# 明细管理
@app.route('/detail')
def detail():
    if 'loggedin' in session:
        page = int(request.args.get('page', 1))
        per_page = 5
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(*) FROM details"
        cursor.execute(query)
        total = cursor.fetchone()['COUNT(*)']
        start = (page-1)*per_page
        end = start + per_page
        query = "SELECT * FROM details"
        cursor.execute(query)
        all_details = cursor.fetchall()
        all_details_list = list(all_details)
        details = all_details_list[start:end]
        pagination = Pagination(all_details, page=page, per_page=per_page, total=total, items=all_details[page - 1])
        context = {
            'pagination': pagination,
            'details': details
        }
        return render_template('明细.html', **context,  user=session)
    return render_template('明细.html', paginate=6, user=session)


# 工资管理
@app.route('/wage')
def wage():
    if 'loggedin' in session:
        page = int(request.args.get('page', 1))
        per_page = 5
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT COUNT(*) FROM salary"
        cursor.execute(query)
        total = cursor.fetchone()['COUNT(*)']
        start = (page-1)*per_page
        end = start + per_page
        query = "SELECT * FROM salary"
        cursor.execute(query)
        all_salary = cursor.fetchall()
        all_salary_list = list(all_salary)
        salary = all_salary_list[start:end]
        pagination = Pagination(all_salary, page=page, per_page=per_page, total=total, items=all_salary[page - 1])
        context = {
            'pagination': pagination,
            'salary': salary
        }
        return render_template('工资管理.html', **context,  user=session)
    return render_template('工资管理.html', paginate=6,  user=session)


# 新增
@app.route('/add_user')
def add_user():
    return render_template('新增.html')


# 退出登录
@app.route('/logout')
def logout():
    # 删除会话数据，这将使用户注销
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.run()

