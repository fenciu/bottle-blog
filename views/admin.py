from bottle import Bottle,jinja2_template as template,jinja2_view as view,static_file,BaseTemplate,request,abort
from plugins.dbconnect import dbConnectPlunin
import os,random,string
import setting

admin=Bottle()

admin.install(setting.db)

BaseTemplate.defaults['url']=admin.get_url

#后台首页
@admin.get('/index/',name='index_url')
@view('./admin/index.html')
def index():
    return dict(name='s')

#后台文章页
@admin.get('/article/',name='article_url')
def article(db):
    data=db.default.post.select('*')
    return template('./admin/article.html',article=data)

@admin.get('/article/add',name='add_article_url')
def add_article(db):
    data_classify=db.default.classify.select('*')
    data_tag=db.default.tag.select('*')
   
   
    return template('./admin/add_article.html',data_classify=data_classify,data_tag=data_tag)

#接受文章数据
@admin.post('/article/add',name='add_article_url')
def add_article(db):
    #验证数据（待补充）
    # data=request.forms.content
    # #data_create=dbs.default.post.bulk_create
    post_dict={}
    for pro in request.forms:
        post_dict[pro]=getattr(request.forms,pro)
        print(pro+":"+getattr(request.forms,pro))
    print(type(request.forms.dict))   
    if 'tag' in request.forms.dict.keys():
        tag_str=','.join(request.forms.dict['tag'])
        post_dict['tag']=tag_str
        
    if post_dict['post_time']=='':
        del post_dict['post_time']
    
    if 'files' in request.forms.dict.keys():
        del post_dict['files']
    print(post_dict)
    post_list=[]
    post_list.append(post_dict)
    data_create=db.default.post.bulk_create(post_list)
    #print(dbs.default.post.bulk_create(post_list).sql)
    #test_data=[{'title': '我的第一个web', 'author': 'admin','tag':'1'}]
    #data_create=dbs.default.post.bulk_create(test_data) 
    
    
    

##上传图片
@admin.post('/article/upload',name='upload_img_url')
def upload():
    upload=request.files.get('files')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.png','.jpg','.jpeg'):
        return abort(code=404)
    else:
        random_name=''.join(random.sample(string.ascii_letters + string.digits, 16))
        
        upload.filename = ''.join((random_name,ext))
    save_path ='./static/post/images/'
    upload.save(save_path) # appends upload.filename automatically
    return upload.filename

@admin.get('/classify/',name='classify_img_url')
def classify():
    return template('./admin/classify.html')

@admin.get('/article/<filename>')
def server_static(filename):
    root_str='./static/post/images/'
    return static_file(filename,root=root_str)

@admin.get('/<namedir0>/<namedir1>/<namedir2>/<namedir3>/<namedir4>/<filename>')
def server_static(filename,namedir1,namedir2,namedir3,namedir4,namedir0):
    root_str='./static/admin/%s/%s/%s/%s/' %(namedir1,namedir2,namedir3,namedir4)
    return static_file(filename,root=root_str)

@admin.get('/<namedir0>/<namedir1>/<namedir2>/<namedir3>/<filename>')
def server_static(filename,namedir1,namedir2,namedir3,namedir0):
    root_str='./static/admin/%s/%s/%s/' %(namedir1,namedir2,namedir3)
    return static_file(filename,root=root_str)

@admin.get('/<namedir0>/<namedir1>/<namedir2>/<filename>')
def server_static(filename,namedir1,namedir2,namedir0):
    root_str='./static/admin/%s/%s/' %(namedir1,namedir2)
    return static_file(filename,root=root_str)

@admin.get('/<namedir0>/<namedir1>/<filename>')
def server_static(filename,namedir1,namedir0):
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