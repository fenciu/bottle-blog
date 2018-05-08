from bottle import Bottle,TEMPLATE_PATH,Route,static_file
from bottle import jinja2_template as template, jinja2_view as view
from views.index import index
from plugins.dbconnect import dbConnectPlunin
from plugins.PyMy import PyMySQLPlugin
TEMPLATE_PATH.remove('./views/')
TEMPLATE_PATH.append('template')
    
#@route('/')
#@route('/hello/<name>')
app=Bottle()
#app.mount('/views/',index)
db=dbConnectPlunin(db='blog',table='post',keyword='db', host='172.16.48.77', port=3306, username='root',password='123456')
app.install(db)
#pymysql = PyMySQLPlugin(user='root',password='123456', db='phpdev')
#app.install(pymysql)
@app.get('/')
def defautl(db):
    #db.default.symbols.get(header='1123')
    
    data=db.default.post.select('*')
    #print(data.title)
    
    return template('./index/index.html',contents=data)
@app.get('/css/<filename>')
def server_static(filename):
    return static_file(filename,root='./static/css/')
@app.get('/images/<filename>')
def server_static(filename):
    return static_file(filename,root='./static/images/')
@app.get('/assets/js/<filename>')
def server_static(filename):
    return static_file(filename,root='./static/js/')
@app.get('/fonts/<filename>')
def server_static(filename):
    return static_file(filename,root='./static/fonts/')
print()
#SimpleTemplate.defaults['get_url']=app.get_url
#app.route('/',callback=hello)
#app.route('/hello/<name>',callback=hello,name='foxx')
#print(app.get_url('foxx'))
#app.get_url('foxx')
#app.get_url('foxx')

#app.run(host='localhost',port=8081,debug=True,reloader=True)
app.run(host='localhost',port=8081,debug=True,reloader=True)