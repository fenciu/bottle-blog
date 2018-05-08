import pymysql.cursors
import inspect

class PyMySQLPlugin(object):
    ''' This plugin passes a pymysql database handle to route callbacks
    that accept a `db` keyword argument. If a callback does not expect
    such a parameter, no connection is made. You can override the database
    settings on a per-route basis. '''

    name = 'pymysql'
    api = 2

    def __init__(self, db, user, password, host='172.16.48.77', charset='utf8mb4', keyword='db'):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.keyword = keyword

    def setup(self, app):
        ''' Make sure that other installed plugins do not affect the same
            keyword argument.'''
        for other in app.plugins:
            if not isinstance(other, PyMySQLPlugin): continue
            if other.keyword == self.keyword:
                raise PluginError("Found another %s plugin with "
                "conflicting settings (non-unique keyword)." % self.name)

    def apply(self, callback, context):
        # Override global configuration with route-specific values.
        #conf = context.config.get('sqlite') or {}
        #dbfile = conf.get('dbfile', self.dbfile)

        # Test if the original callback accepts a 'db' keyword.
        # Ignore it if it does not need a database handle.
        args = inspect.getargspec(context.callback)[0]
        if self.keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            # Connect to the database
            db = pymysql.connect(host=self.host,
                    user=self.user,
                    password=self.password,
                    db=self.db,
                    charset=self.charset,
                    cursorclass=pymysql.cursors.DictCursor)

            # Add the connection handle as a keyword argument.
            kwargs[self.keyword] = db

            try:
                rv = callback(*args, **kwargs)
                #if autocommit: db.commit()
            #except sqlite3.IntegrityError, e:
                #db.rollback()
                #raise HTTPError(500, "Database Error", e)
            finally:
                db.close()
            return rv

        # Replace the route callback with the wrapped one.
        return wrapper