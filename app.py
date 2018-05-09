from bottle import Bottle,TEMPLATE_PATH,Route,static_file
from bottle import jinja2_template as template, jinja2_view as view
from views.admin import admin
from views.index import index
from plugins.dbconnect import dbConnectPlunin
from plugins.PyMy import PyMySQLPlugin
TEMPLATE_PATH.remove('./views/')
TEMPLATE_PATH.append('template')
    
#@route('/')
#@route('/hello/<name>')
app=Bottle()


db=dbConnectPlunin(db='blog',table='post',keyword='db', host='172.16.48.77', port=3306, username='root',password='123456')
app.install(db)
app.mount('/views/',index)
app.mount('/admin/',admin)
@app.get('/')
def defautl(db):
    #db.default.symbols.get(header='1123')
    
    data=db.default.post.select('*')
    #print(data.title)
    
    return template('./index/index.html',contents=data)

@app.get('/<namedir>/<filename>')
def server_static(filename):
    root_str='./static/%s/' %namedir
    return static_file(filename,root=root_str)
print()
#SimpleTemplate.defaults['get_url']=app.get_url
#app.route('/',callback=hello)
#app.route('/hello/<name>',callback=hello,name='foxx')
#print(app.get_url('foxx'))
#app.get_url('foxx')
#app.get_url('foxx')

#app.run(host='localhost',port=8081,debug=True,reloader=True)
app.run(host='localhost',port=8081,debug=True)