from bottle import Bottle,jinja2_template as template,jinja2_view as view,static_file
from plugins.dbconnect import dbConnectPlunin

admin=Bottle()
dbs=dbConnectPlunin(db='blog',table='post',keyword='dbs', host='172.16.48.77', port=3306, username='root',password='123456')
admin.install(dbs)

@admin.get('/index/',name='index')
@view('./admin/index.html')
def index():
    
    return dict(name='s')


@admin.get('/index/article/',name='article')
def article(dbs):
    
    data=dbs.default.post.select('*')
    return template('./admin/article.html',article=data)

@admin.get('/index/<name>/<filename>')
def server_static(filename,name):
    
    root_str='./static/%s/' %name
    
    return static_file(filename,root=root_str)

@admin.get('/index/<namedir1>/<namedir2>/<filename>')
def server_static(filename,namedir1,namedir2):
    root_str='./static/%s/%s/' %(namedir1,namedir2)
    return static_file(filename,root=root_str)



@admin.get('/index/<filename>')
def server_static(filename):
    
    
    return static_file(filename,root='./template/admin/')