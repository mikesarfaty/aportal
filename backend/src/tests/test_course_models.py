import unittest
from aportalserver.models.sqlutils import get_conn
import aportalserver.models

class TestCourses(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        conn = get_conn()
        cls._conn = conn
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users")
            cur.execute("DELETE FROM courses")
            cur.execute("DELETE FROM taken_courses")

    @classmethod
    def tearDownClass(cls):
        cls._conn.close()

    def setUp(self):
        course1 = (1, "CS", "2500", "fundies 1", "CCIS")
        course2 = (2, "LW", "1001", "we hate capitalism", "LAW")
        course3 = (3, "BS", "8000", "we love capitalism", "DMSB")
        user1 = (1, 'mike sarfaty', '2021', 's1', 'computer science', '', 'mikesarfaty', 'a note',)
        user2 = (2, 'david rans', '2021', 'spr', 'finance', '', 'davidrans', 'another note',)
        user3 = (3, 'nick pechie', '2021', 'spr', 'computer engineering', '', 'nickpechie', 'user3 note',)
        taken_course1 = (1, 1, 1, 'SPR', '2021', None, None)
        taken_course2 = (2, 2, 1, 'FALL', '2020', None, None)
        taken_course3 = (3, 3, 1, 'S1', '2016', None, None)
        taken_course4 = (4, 2, 2, 'FALL', '2021', None, None)
        taken_course5 = (5, 3, 2, 'S2', '2050', None, None)
        taken_course6 = (6, 3, 3, 'SPR', '2018', None, None)
        with self._conn.cursor() as cur:
            cur.execute(f"INSERT INTO users VALUES {user1}, {user2}, {user3}")
            cur.execute(f"INSERT INTO courses VALUES {course1}, {course2}, {course3}")
            cur.execute("INSERT INTO taken_courses VALUES %s, %s, %s, %s, %s, %s",
                        (
                            taken_course1,
                            taken_course2,
                            taken_course3,
                            taken_course4,
                            taken_course5,
                            taken_course6
                        ))

    def tearDown(self):
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM users;")
            cur.execute("DELETE FROM courses;")
            cur.execute("DELETE FROM taken_courses;")

    def test_it_inserts_ok_lol(self):
        self.assertTrue(True)
