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

##首页和分页(五篇文章)
@app.get('/')
@app.get('/page/<count:int>',name='page_url')#翻页路由 count页数 默认1
def defautl(db,count=1):
    
    str_sql="select post.*,group_concat(tag.name) as tag_name,classify.name as classify_name from post, tag,classify where find_in_set(tag.id, post.tag)  and post.show='off' and classify.id=post.classify group by post.id"
    data=db.default.fetchall_dict(str_sql)
    fetch_data_count=db.default.execute(str_sql)[0]
    fetch_data=data[(count-1)*5:count*5]
    max_count=fetch_data_count/5 if (fetch_data_count%5==0) else fetch_data_count//5+1 #最大页数
    return template('./index/index.html',contents=fetch_data,max_count=max_count,count=count)

@app.get('/post/<id:int>',name='post_url')
def Show_post(db,id):
    str_sql="select post.*,group_concat(tag.name) as tag_name,classify.name as classify_name from post, tag,classify where find_in_set(tag.id, post.tag)  and post.show='off' and post.id=%s and classify.id=post.classify group by post.id" %id
    data=db.default.fetchone_dict(str_sql)
    


    return template('./article/single.html',contents=data)


@app.get('/post/<filename>')
def server_static(filename):
    root_str='./static/post/images/'
    return static_file(filename,root=root_str)

@app.get('/<namedir>/<filename>')
def server_static(filename,namedir):
    root_str='./static/%s/' %namedir
    return static_file(filename,root=root_str)








#SimpleTemplate.defaults['get_url']=app.get_url
#app.route('/',callback=hello)
#app.route('/hello/<name>',callback=hello,name='foxx')
#print(app.get_url('foxx'))
#app.get_url('foxx')
#app.get_url('foxx')

#app.run(host='localhost',port=8081,debug=True,reloader=True)
app.run(host='localhost',port=8081,debug=True)