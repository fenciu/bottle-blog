from bottle import TEMPLATE_PATH
from plugins.dbconnect import dbConnectPlunin



##模板路径
TEMPLATE_PATH.remove('./views/')
TEMPLATE_PATH.append('template')

##数据库
db_config={
    'db':'blog',
    'table':'*',
    'keyword':'db',
    'host':'',
    'port':3306,
    'username':'root',
    'password':'123asdzxc',
    'charset':'utf8',
    'autocommit':True,
    'pool_size':8,
    'wait_timeout':30
}
db=dbConnectPlunin(db_config)