from bottle import Bottle,jinja2_template as template,jinja2_view as view,static_file,BaseTemplate
from plugins.dbconnect import dbConnectPlunin

admin=Bottle()
dbs=dbConnectPlunin(db='blog',table='post',keyword='dbs', host='172.16.48.77', port=3306, username='root',password='123456')
admin.install(dbs)

BaseTemplate.defaults['url']=admin.get_url

#后台首页
@admin.get('/index/',name='index_url')
@view('./admin/index.html')
def index():
    
    return dict(name='s')

#后台文章页
@admin.get('/article/',name='article_url')
def article(dbs):
    
    data=dbs.default.post.select('*')
    return template('./admin/article.html',article=data)




#静态资源

# @admin.get('/<dirname1>/<dirname2>/<filepath:path>',name='static_file_url')
# def server_static(dirname1,dirname2,filepath):
#     root_str='./static/%s/' %(dirname2)
#     print(root_str)
#     return static_file(filepath,root=root_str)

#临时静态资源调试
@admin.get('/<dirname>/<filename>',name='debug')
def server_static(dirname,filename):
    
    
    return static_file(filename,root='./template/admin/')