#导入数据库模块
import pymysql
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用
from flask import Flask
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request
import traceback
from werkzeug.utils import secure_filename
from flask import Flask,render_template,jsonify,request
from flask import request,jsonify,send_from_directory,abort,url_for,redirect
import time
import os
import base64
import csv
import sys
import codecs
import MySQLdb
import importlib

#传递根目录
app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 设置文件上传的目标文件夹
basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前项目的绝对路径

ALLOWED_EXTENSIONS = set(['txt','png','jpg','xls','JPG','PNG','xlsx','gif','GIF','csv'])



# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

# 用于测试上传，稍后用到
@app.route('/upload')
def upload_test():
    return render_template('upload.html')


#默认路径访问登录页面
@app.route('/')
def login():
    return render_template('login.html')

#默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('register.html')

@app.route('/find')
def find():
    return render_template('find.html')

#获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
#把用户名和密码注册到数据库中

    ##
    #连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost","root","15871433996","homework" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO user(username, pwd) VALUES ("+request.args.get('username')+", "+request.args.get('password')+")"

    try:
        # 执行sql语句
        cursor.execute(sql)
         #注册成功之后跳转到登录页面
        # 提交到数据库执行
        db.commit()
        return render_template('/login.html')
    except:
        #抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return render_template('/register.html')
    # 关闭数据库连接
    db.close()


# 获取登录参数及处理
@app.route('/login')
def getLoginRequest():
#查询用户名及密码是否匹配及存在


    #连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost","root","15871433996","homework" )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from user where username="+request.args.get('username')+" and pwd="+request.args.get('password')+""

    #test
    print(request.args.get('username'))
    print(request.args.get('password'))

    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)!=0:
            return render_template('upload.html')
        else:
            return '用户名或密码不正确'
        # 提交到数据库执行
        db.commit()
    except:

        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()

        return render_template("/login.html")

    # 关闭数据库连接
    db.close()


@app.route('/main')
def get_main():
    return 'nihao'

@app.route('/finder')
def getfind():
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "15871433996", "homework")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    #sql = "select * from hp where site = "+ request.args.get("site2")+" and machine=" + request.args.get(
        #'machine')+ " and stem_no = "+ request.args.get('stem_no')+ "  and log_no = "+request.args.get('log_no') +""

    #sql = "select * from hp where machine = "+request.args.get('machine')+""

    formname = request.args.get('formname')

    sql = "select * from %s where site = '%s' and machine = '%s' and stem_no = '%s' and log_no = '%s'" % \
          (formname,request.args.get('site'),request.args.get('machine'),request.args.get('stem_no'),request.args.get('log_no'))

    print(type(request.args.get('site')))
    print(request.args.get('stem_no'))

    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()

        for x in range(len(results)):
            print(results[x])
        if len(results) != 0:
            return render_template('find.html',name=results)
        else:
            return '没有符合您条件的信息'

        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()

        return "搜索失败"
    # 关闭数据库连接
    db.close()

@app.route('/getformname')
def getformname():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='15871433996',
        db='homework',
    )

    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    #create = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'

    sql = 'show tables'
    cursor.execute(sql)
    results = cursor.fetchall()
    results2 = []

    for x in results:
        results2.append(x)
    cursor.close()

    return render_template('find.html', formname=results2)

@app.route('/getformname2')
def getformname2():
    #数据库配置
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='15871433996',
        db='homework',
    )

    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    #create = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'

    #查看所有数据库的表名
    sql = 'show tables'
    cursor.execute(sql)
    results = cursor.fetchall()
    results2 = []

    for x in results:
        results2.append(x)
    cursor.close()

    return render_template('data_output.html', formname=results2)


# 上传文件
#@app.route('/api/upload')
@app.route('/api/upload', methods=['POST'], strict_slashes=False)
def upload():

    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])  # 拼接成合法文件夹地址

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)  # 文件夹不存在就创建

    f = request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值

    print(f.filename)

    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = f.filename
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time) + '.' + ext  # 修改文件名
        f.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录


    importlib.reload(sys)

    #print(request.args.get('location'))
    #print('E:/testflask/upload/' + new_filename)
    #csv_filename = request.args.get('location')
    #csv_filename = 'E:/TestPython/HP2014-0014.csv'
    #csv_filename = 'E:/new_work/upload/1526354907.csv'

    #new_filename = '1526354907.csv'
    csv_filename = "E:/new_work/upload/" + new_filename
    #csv_filename = 'E:/new_work/upload/1526354907.csv'
    #database = request.args.get('Database')
    data = 'homework'
    #table_name = request.args.get('Tables')
    table_name = request.form['Tables']
    #table_name = new_filename.rsplit('.',1)[0]
    #table_name = '1526354907'
    print('table name')
    print(type(table_name))

    file = codecs.open(csv_filename, 'r', 'utf-8')
    reader = file.readline()
    b = reader.split(',')
    colum = ''
    for a in b:
        colum = colum + a + ' varchar(255),'

    colum = colum[:-1]

    create = 'create table if not exists ' + table_name + ' ' + '(' + colum + ')' + ' DEFAULT CHARSET=utf8'

    data = 'LOAD DATA LOCAL INFILE \'' + csv_filename + '\' INTO TABLE ' + table_name + ' character set utf8 FIELDS TERMINATED BY \',\' ENCLOSED BY \'\"\' LINES TERMINATED BY \'' + r'\r\n' + '\' IGNORE 1 LINES;'

    conn = MySQLdb.connect(
        #数据库的配置
        host='localhost',
        port=3306,
        user='root',
        passwd='15871433996',
        db='homework',
        local_infile=1
    )

    conn.set_character_set('utf8')
    cursor = conn.cursor()
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    cursor.execute(create)
    cursor.execute(data)
    cursor.rowcount

    conn.commit()
    cursor.close()

    return render_template("/upload.html")

@app.route('/data_output')
def data():
    return render_template("/data_output.html")

@app.route('/data')
def out_data():

    return 'ok'

@app.route("/download/<path:filename>")
def downloader(filename):

    dirpath = os.path.join(app.root_path, 'upload')  # 这里是下在目录，从工程的根目录写起，比如你要下载static/js里面的js文件，这里就要写“static/js”
    return send_from_directory(dirpath, filename, as_attachment=True)  # as_attachment=True 一定要写，不然会变成打开，而不是下载

@app.route("/down")
def down():

    #获取所要处理的数据表的名字
    selctform = request.args.get("getname")

    #连接数据库
    conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="15871433996", db="homework", charset='utf8')
    cur = conn.cursor()

    conf = "set @@sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'";

    cur.execute(conf)

    #》》》》》这里需要更改表名
    # 执行数据库的操作cur.execute
    sql = "select site,machine,stem_no,count(log_no),sum(log_no) wholeloglength,AVG(log_no) aveloglength from %s group by stem_no;"%(selctform)

    #执行查询
    cur.execute(sql)
    rows = cur.fetchall()
    results = []

    #新建一个文件，这里根据实际路径配置
    f = open('E:/new_work/upload/data.csv', 'w')
    writer = csv.writer(f)

    #写入列名
    writer.writerow(["site", "machine", "stem_no", "num(log)","wholeloglength", "aveloglength"])
    for x in rows:
        for y in range(len(x)):
            print(x[y])
            results.append(str(x[y]))

        print("here")
        print(type(results))
        writer.writerows([results])
        results = []
        # f.write(str(x[y])+' ')
        # f.write('\n')

    # f.write('\n')


    #第二个查询语句
    sql2 = "select product_de,count(*) 总数,max(volob),min(volob) from %s group by product_de;"%(selctform)

    #执行第二个查询
    cur.execute(sql2)
    rows2 = cur.fetchall()

    results2 = []

    #写入新的字段
    writer.writerow(["product_de字段", "NUMS", "MAXVOLBO", "MINVOLBO"])

    for x in rows2:
        for y in range(len(x)):
            print(x[y])
            results2.append(str(x[y]))
            # f.write(str(x[y]) + ' ')

        writer.writerows([results2])
        results2 = []
        # f.write('\n')

    # print(rows2)

    f.close()
    conn.close()

    #这里需要传入需要下载的文件名
    login_url = url_for('downloader', filename='data.csv')

    return redirect(login_url)

@app.route("/data_output.html")
def r():
    return render_template("data_output.html")

if __name__ == '__main__':
    app.run(debug=True)
