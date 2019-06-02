LOCK_MODES = (
    'ACCESS SHARE',
    'ROW SHARE',
    'ROW EXCLUSIVE',
    'SHARE UPDATE EXCLUSIVE',
    'SHARE',
    'SHARE ROW EXCLUSIVE',
    'EXCLUSIVE',
    'ACCESS EXCLUSIVE',
)


def acquire_lock(model_or_table, lock='ACCESS EXCLUSIVE', using=None):
    if lock not in LOCK_MODES:
        raise ValueError('%s is not a PostgreSQL supported lock mode.' % lock)
    from django.db import connections, connection, router
    try:
        table_name = model_or_table._meta.db_table
        conn_name = using or router.db_for_write(model_or_table)
    except AttributeError:
        table_name = str(model_or_table)
        conn_name = using
    if conn_name:
        conn = connections[conn_name]
        cursor = conn.cursor()
    else:
        cursor = connection.cursor()
        conn = connection

    cursor.execute(
        'LOCK TABLE %s IN %s MODE' % (table_name, lock)
    )
    return conn


class lock:
    def __init__(self, model_or_table, mode='ACCESS EXCLUSIVE', using=None):
        self.model_or_table = model_or_table
        self.mode = mode
        self.using = using

    def __enter__(self):
        acquire_lock(self.model_or_table, self.mode, self.using)

    def __exit__(self, type, value, traceback):
        pass


def require_lock(model_or_table, lock='ACCESS EXCLUSIVE', using=None):
    """
    Decorator for PostgreSQL's table-level lock functionality

    Example:
        @transaction.atomic
        @require_lock(MyModel, 'ACCESS EXCLUSIVE')
        def myview(request)
            ...

    PostgreSQL's LOCK Documentation:
    http://www.postgresql.org/docs/8.3/interactive/sql-lock.html
    """
    def require_lock_decorator(view_func):
        def wrapper(*args, **kwargs):
            acquire_lock(model_or_table, lock, using)
            return view_func(*args, **kwargs)
        return wrapper
    return require_lock_decorator
