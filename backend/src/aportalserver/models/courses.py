from aportalserver.models.sqlutils import get_conn

class Course:
    def __init__(self, course_id, conn=None):
        if conn is None:
            self.conn = get_conn()
        else:
            self.conn = conn
        self.course_id = course_id

    def select(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM courses WHERE course_id=%s" % (self.course_id,))
            return cur.fetchone()

    def retrieve_taken_courses(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM taken_courses NATURAL JOIN users WHERE course_id=%s" % (self.course_id,))
            return cur.fetchall()

def create_new_course(course_prefix, course_number, course_fullname):
    with get_conn().cursor() as cur:
        cur.execute("""
        INSERT INTO courses (course_prefix, course_number, course_fullname)
        VALUES (%s, %s, %s)
        """ % (course_prefix, course_number, course_fullname,))
        return True


class TakenCourse:
    def __init__(self, taken_course_id, conn=None):
        if conn is None:
            self.conn = get_conn()
        else:
            self.conn = conn
        self.taken_course_id = taken_course_id

    def select(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM taken_courses WHERE taken_course_id=%s" % (self.course_id,))
            return cur.fetchone()