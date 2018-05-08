from bottle import template,route,Bottle,url,TEMPLATE_PATH,view


index=Bottle()
@index.route('/hello/<name>.html',name='foxx')
@view('hello')
def hello(name="null"):
    #return template('./template/hello',name=name,get_url=app.get_url('foxx',name=''))
    #print(app.get_url('foxx',name=''))
    print('index:'+__name__+"   ")
    
    print(index.get_url('foxx',name=''))


    return dict(name=name,index=index)


@index.route('/godbye/',name='gb')
def godbye():
    return __name__
