from aportalserver.models.sqlutils import get_conn
import secrets

class User:
    def __init__(self, user_id, conn=None):
        if conn is None:
            self.conn = get_conn()
        else:
            self.conn = conn
        self.user_id = user_id

    def select(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE user_id=%s" % (self.user_id,))
            return cur.fetchone()

    def taken_courses_by_user(self):
        with self.conn.cursor() as cur:
            cur.execute("""
            SELECT *
            FROM taken_courses
            NATURAL JOIN courses
            WHERE taken_courses.user_id=%s
            """ % self.user_id)
            return cur.fetchall()

    def update(self, update_cols):
        update_sets = []
        if update_cols.get('user_id'):
            del update_cols['user_id']
        for attr in update_cols.keys():
            update_sets.append(f"{attr}='{update_cols[attr]}'")
        update_str = ', '.join(update_sets)
        if update_str:
            stmt = 'UPDATE users SET %s WHERE user_id=%s;' % (update_str, self.user_id,)
            with self.conn.cursor() as cur:
                cur.execute(stmt)
        return self.select()

def create_user(kwargs):
    """
    Override, skips registration routine, create a user. Fields/Vals SQL Safe

    SQL-Injection Safety probably breaks this function.

    :Returns dict - The User
    """
    fields = f'({",".join(kwargs.keys())})'
    values = f'({",".join(kwargs.values())})'
    stmt = 'INSERT INTO users %s VALUES %s;' % (fields, values,)
    with get_conn().cursor() as cur:
        cur.execute(stmt)
        return kwargs


def register_user(registration_hash, graduating_year, graduating_semester, major, pw_hash):
    """
    Calls the MySQL register_user procedure defined in migration 03.new-users.sql
    :Returns Bool Whether the operation was successful
    """
    with get_conn().cursor() as cur:
        cur.execute("CALL register_user('%s', '%s', '%s', '%s', '%s')" % (registration_hash, graduating_year, graduating_semester, major, pw_hash))
        cur.execute("SELECT * FROM users WHERE username=(SELECT username FROM unregistered_users WHERE registration_hash='%s')" % registration_hash)
        return cur.fetchone()


def preregister_user(username, full_name):
    """
    Creates a pre-registration for a user
    :Returns Bool Whether the operation was successful
    """
    registration_hash = secrets.token_hex(32)
    with get_conn().cursor() as cur:
        cur.execute("""
            INSERT INTO unregistered_users (
                username, full_name, registration_hash
            ) VALUES (
                '%s', '%s', '%s'
            )""" % (username, full_name, registration_hash,))
        return True

def get_users_registration_hash(username):
    """
    Gets an unregistered user's registration hash
    :Returns str the registration_hash if the user exists, otherwise empty str
    """
    with get_conn().cursor() as cur:
        cur.execute("SELECT registration_hash FROM unregistered_users WHERE username=%s" % username)
        r = cur.fetchone()
        if not r:
            return ''
        return r['registration_hash']

def all_users():
    with self.conn.cursor as cur:
        cur.execute("""
        SELECT * FROM users;
        """)
        return cur.fetchall()
