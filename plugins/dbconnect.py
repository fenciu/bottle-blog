import lorm
import pymysql
import inspect

class dbConnectPlunin(object):
    name='mysqlconnect'
    api=2
    def __init__(self,db,table,keyword,host,port,username,password):
        self.db=db
        self.table=table
        self.keyword=keyword
        self.host=host
        self.port=port
        self.username=username
        self.password=password

    def setup(self,app):
        for other in app.plugins:
            if not isinstance(other,dbConnectPlunin):continue
            if other.keyword == self.keyword:
                raise PluginError("Found another %s plugin with "
                "conflicting settings (non-unique keyword)." % self.name)
    
    def apply(self,callback,context):
        args = inspect.getfullargspec(context.callback)[0]
        if self.keyword not in args:
            return callback
        
        def wrapper(*args,**kwargs):
            db=lorm.Hub(pymysql)
            db.add_pool('default',
                host=self.host,
                port=self.port,
                user=self.username,
                passwd=self.password,
                db=self.db,
                autocommit=True,
                pool_size=8,
                wait_timeout=30) 
            kwargs[self.keyword] = db
            try:
                rvs=callback(*args,**kwargs)
                

            except :
                print('error')

            return rvs
        return wrapper
