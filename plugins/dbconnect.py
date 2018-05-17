import lorm
import pymysql
import inspect

class dbConnectPlunin(object):
    name='mysqlconnect'
    api=2
    def __init__(self,config):
        self.db=config['db']
        self.table=config['table']
        self.keyword=config['keyword']
        self.host=config['host']
        self.port=config['port']
        self.username=config['username']
        self.password=config['password']
        self.charset=config['charset']
        self.autocommit=config['autocommit']
        self.pool_size=config['pool_size']
        self.wait_timeout=config['wait_timeout']

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
                charset=self.charset,
                autocommit=self.autocommit,
                pool_size=self.pool_size,
                wait_timeout=self.wait_timeout) 
            kwargs[self.keyword] = db
            
            rv=callback(*args,**kwargs)
            
                

            return rv
        return wrapper
