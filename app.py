from bottle import Bottle,TEMPLATE_PATH,Route,static_file,BaseTemplate
from bottle import jinja2_template as template, jinja2_view as view
from views.admin import admin
from views.index import index
import setting


#@route('/')
#@route('/hello/<name>')
app=Bottle()

BaseTemplate.defaults['url']=app.get_url

app.install(setting.db)
app.mount('/views/',index)
app.mount('/admin/',admin)

##首页
@app.get('/')
def defautl(db):
    #db.default.symbols.get(header='1123')
    
    data=db.default.post.select('*')
  
    #print(data.title)
    
    return template('./index/index.html',contents=data)

##翻页
@app.get('/page/<count:int>',name='page_url')
def page(db,count):
    fetch_data=db.default.post.filter(show='off')[(count-1)*5:count*5]
    data=db.default.post.select('*')
    for fetch in fetch_data:
        print(fetch)
    return template('./index/index.html',contents=data,count=count)

@app.get('/<namedir>/<filename>')
def server_static(filename,namedir):
    root_str='./static/%s/' %namedir
    return static_file(filename,root=root_str)


@app.route('/s')
def text(db):
    print('s')
    return 's'


#SimpleTemplate.defaults['get_url']=app.get_url
#app.route('/',callback=hello)
#app.route('/hello/<name>',callback=hello,name='foxx')
#print(app.get_url('foxx'))
#app.get_url('foxx')
#app.get_url('foxx')

#app.run(host='localhost',port=8081,debug=True,reloader=True)
app.run(host='localhost',port=8081,debug=True)