from .sqlutils import MyConn as Conn

class Users:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conn = Conn()

    def taken_courses_by_user(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT *
            FROM taken_courses
            NATURAL JOIN courses
            WHERE taken_courses.user_id=%s
            """ % self.user_id)
            return cur.fetchall()

    def all_users():
        with self.conn.cursor as cur:
            cur.execute("""
            SELECT * FROM users;
            """)
            return cur.fetchall()

    def info(self):
        with self.conn.cursor as cur:
            cur.execute("""
            SELECT * FROM users WHERE user_id=%s;
            """ % self.user_id)
            return cur.fetchall()

    def create_user(kwargs):
        fields = f'({",".join(kwargs.keys())})'
        values = f'({",".join(kwargs.values())})'
        stmt = 'INSERT INTO users %s VALUES %s;' % (fields, values,)
        with self.conn.cursor() as cur:
            cur.execute(stmt)
            return kwargs

    def update_user(uid, kwargs):
        update_sets = []
        for attr in kwargs.keys() if attr != 'user_id':
            update_sets.append(f'{attr}={kwargs[attr]}')
        update_str = ', '.join(update_sets)
        stmt = 'UPDATE users SET %s WHERE user_id=%s;' % (update_str, uid,)
        with self.conn.cursor() as cur:
            cur.execute(stmt)
            cur.execute("SELECT * FROM users WHERE user_id=%s" % uid)
            return cur.fetchone()
