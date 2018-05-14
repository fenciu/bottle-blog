from bottle import Bottle,jinja2_template as template,jinja2_view as view,static_file,BaseTemplate,request
from plugins.dbconnect import dbConnectPlunin

admin=Bottle()
dbs=dbConnectPlunin(db='blog',table='*',keyword='dbs', host='', port=3306, username='root',password='123asdzxc')
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

@admin.get('/article/add',name='add_article_url')
def add_article(dbs):
    data_classify=dbs.default.classify.select('*')
    data_tag=dbs.default.tag.select('*')
   
   
    return template('./admin/add_article.html',data_classify=data_classify,data_tag=data_tag)

#接受文章数据
@admin.post('/article/add',name='add_article_url')
def add_article(dbs):
    #验证数据（待补充）
    data=request.forms.content
    data_create=dbs.default.post.bulk_create
    post_dict={}
    for pro in request.forms:
        #post_dict[pro]=getattr(request.forms,pro)
        print(pro+":"+getattr(request.forms,pro))
       

    #print(post_dict)
    #data_create=dbs.default.post.bulk_create(post_dict)
    
    return post_dict
    
@admin.get('/article/<namedir1>/<namedir2>/<namedir3>/<namedir4>/<filename>')
def server_static(filename,namedir1,namedir2,namedir3,namedir4):
    root_str='./static/admin/%s/%s/%s/%s/' %(namedir1,namedir2,namedir3,namedir4)
    return static_file(filename,root=root_str)

@admin.get('/article/<namedir1>/<namedir2>/<namedir3>/<filename>')
def server_static(filename,namedir1,namedir2,namedir3):
    root_str='./static/admin/%s/%s/%s/' %(namedir1,namedir2,namedir3)
    return static_file(filename,root=root_str)

@admin.get('/article/<namedir1>/<namedir2>/<filename>')
def server_static(filename,namedir1,namedir2):
    root_str='./static/admin/%s/%s/' %(namedir1,namedir2)
    return static_file(filename,root=root_str)

@admin.get('/article/<namedir1>/<filename>')
def server_static(filename,namedir1):
    root_str='./static/admin/%s/' %(namedir1)
    return static_file(filename,root=root_str)



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