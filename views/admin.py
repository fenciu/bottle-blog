from bottle import Bottle,jinja2_template as template,jinja2_view as view,static_file,BaseTemplate,request,response,abort,TEMPLATES,redirect
from plugins.dbconnect import dbConnectPlunin
import os,random,string,hashlib
import setting

admin=Bottle()

admin.install(setting.db)

BaseTemplate.defaults['urls']=admin.get_url
TEMPLATES.clear()

##后台cookie检测
def check_login(db,request):
    if request.get_cookie("id",secret="2018")==None:
        redirect('/admin/login/')
    else:         
        re=request.get_cookie("id",secret="2018")
        re1,re2=re.split(':', 1 )
        fetch_data=db.default.Conadmin.filter(username=re1,userpass=re2).select('id').first()
        if not fetch_data:
            redirect('/admin/login/')

#登陆界面
@admin.get('/login/',name='login_url')
def login_view():
    return template('./admin/login.html')

@admin.post('/login/')
def login_post(db):
    sec=hashlib.blake2b()
    sec.update(request.forms.userpass.encode(encoding='utf-8'))
    username=request.forms.username
    userpass=sec.hexdigest()
    fetch_data=db.default.Conadmin.filter(username=username,userpass=userpass).select('login_time').first()
    if fetch_data:
        response.set_cookie("id",username+':'+userpass,secret="2018",httponly=True,path='/admin')
        re=request.get_cookie("id",secret="2018")
        print(re)
        redirect(admin.get_url('index_url'))
    else:
        return 'fail'
#退出登陆
@admin.get('/logout/',name='logout_url')
def logout():
    response.delete_cookie(key='id',path='/admin')
    redirect(admin.get_url('login_url'))

#后台首页
@admin.get('/index/',name='index_url')
def index(db):
    setting.check_login(db,request)
    
    return template('./admin/index.html',act_index='active')

#后台文章页
@admin.get('/article/',name='article_url')
def article(db):
    setting.check_login(db,request)
    data=db.default.post.select('*')
    return template('./admin/article.html',article=data,act_article='active')
#添加文章
@admin.get('/article/add',name='add_article_url')
def add_article(db):
    setting.check_login(db,request)
    data_classify=db.default.classify.select('*')
    data_tag=db.default.tag.select('*')
    return template('./admin/add_article.html',data_classify=data_classify,data_tag=data_tag,act_article='active')

#修改文章
@admin.get('/article/modify=<id:int>')
def modify_article(id,db):
    setting.check_login(db,request)
    data=db.default.post.filter(id=id).first()
    data_tag=db.default.tag.select('*')
    data_classify=db.default.classify.select('*')
    return template('./admin/modify.html',content=data,data_tag=data_tag,data_classify=data_classify)
#接受修改文章
@admin.post('/article/modify=<id:int>',name='modify_url')
def modify_article(id,db):
    setting.check_login(db,request)
    post_dict={}
    for pro in request.forms:
        post_dict[pro]=getattr(request.forms,pro)
        print(pro+":"+getattr(request.forms,pro))
      
    if 'tag' in request.forms.dict.keys():
        tag_str=','.join(request.forms.dict['tag'])
        post_dict['tag']=tag_str


    if post_dict['post_time']=='':
        del post_dict['post_time']
    
    if 'files' in request.forms.dict.keys():
        del post_dict['files']
    post_list=[]
    post_list.append(post_dict)
    data_update=db.default.post.filter(id=id).bulk_update(post_list)

    
#分类
@admin.get('/classify/',name='classify_url')
def teclassify(db):
    setting.check_login(db,request)
    return template('./admin/classify.html' ,act_classify='active')

#标签
@admin.get('/tag/',name='tag_url')
def tag(db):
    setting.check_login(db,request)
    return template('./admin/tag.html',act_tag='active')



#接受文章数据
@admin.post('/article/add',name='add_article_url')
def add_article(db):
    setting.check_login(db,request)
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
    post_list=[]
    post_list.append(post_dict)
    data_create=db.default.post.bulk_create(post_list)
    
    

##上传图片
@admin.post('/article/upload',name='upload_img_url')
def upload(db):
    setting.check_login(db,request)
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