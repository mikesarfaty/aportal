import unittest
import aportalserver.models as models
from aportalserver.models.sqlutils import get_conn

User = models.users.User
users = models.users

class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._conn = get_conn()

    @classmethod
    def tearDownClass(cls):
        with cls._conn.cursor() as cur:
            cur.execute("""
                delete from users where user_id in (1, 2, 3);
            """)
        cls._conn.close()

    def setUp(self):
        with self._conn.cursor() as cur:
            cur.execute("DELETE FROM users;")
        u1 = (1, 'mike sarfaty', '2021', 's1', 'computer science', '', 'mikesarfaty', 'a note',)
        u2 = (2, 'david rans', '2021', 'spr', 'finance', '', 'davidrans', 'another note',)
        u3 = (3, 'nick pechie', '2021', 'spr', 'computer engineering', '', 'nickpechie', 'user3 note',)
        with self._conn.cursor() as cur:
            cur.execute(f"""
                insert into users
                (user_id, full_name, graduating_year, graduating_semester, major, pw_hash, username, notes)
                values {u1}, {u2}, {u3};
            """)
            cur.execute("SELECT * FROM users")

    def test_user_select_connpassing(self):
        u1 = User(1, conn=self._conn)
        self.assertEqual(u1.select()['username'], 'mikesarfaty')

    def test_user_select_no_connpassing(self):
        u2 = User(2)
        self.assertEqual(u2.select()['username'], 'davidrans')

    def test_user_select_user_does_not_exist(self):
        u3 = User(5)
        self.assertIsNone(u3.select())

    def test_update_user_updating_uid_fails(self):
        User(1).update({'user_id': 2})
        self.assertEqual(User(1).select()['username'], 'mikesarfaty')

    def test_update_user_username(self):
        User(1).update({'username': 'mikesarfaty2'})
        self.assertEqual(User(1).select()['username'], 'mikesarfaty2')


class TestPreregisterUserModelAndFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._conn = get_conn()
        with cls._conn.cursor() as cur:
            cur.execute("""
                DELETE FROM users WHERE user_id > 0;
            """)
            cur.execute("DELETE FROM unregistered_users;")

    @classmethod
    def tearDownClass(cls):
        with cls._conn.cursor() as cur:
            cur.execute("""
                DELETE FROM users WHERE user_id IN (1, 2, 3);
            """)
            cur.execute("DELETE FROM unregistered_users WHERE username = 'mikesarfaty';")
        cls._conn.close()
    
    def setUp(self):
        with self._conn.cursor() as cur:
            cur.execute("""
                DELETE FROM users;
            """)
            cur.execute("DELETE FROM unregistered_users WHERE username = 'mikesarfaty';")

    def test_pregister_user_works(self):
        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM unregistered_users")
            r = cur.fetchall()
            self.assertEqual(len(r), 0)
        users.preregister_user('mikesarfaty', 'mike sarfaty')
        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM unregistered_users")
            r = cur.fetchone()
            self.assertEqual(r['username'], 'mikesarfaty')

    def test_registering_preregistered_user(self):
        users.preregister_user('mikesarfaty', 'mike sarfaty')
        with self._conn.cursor() as cur:
            cur.execute("SELECT * FROM unregistered_users WHERE username='%s'" % ('mikesarfaty',))
            r = cur.fetchone()
            registration_hash = r['registration_hash']
        user = users.register_user(registration_hash, '2021', 'S1', 'computer science', 'a')
        self.assertEqual(User(user['user_id']).select()['username'], 'mikesarfaty')



if __name__ == '__main__':
    unittest.main()