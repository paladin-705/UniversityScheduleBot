import sys
import unittest

sys.path.append('../')

from config import config
import scheduledb


class TestScheduleDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = scheduledb.ScheduleDB(config)

    def tearDown(self):
        self.db.clear_tables()

    def test_add_organization(self):
        tag = self.db.add_organization("test_organization", "test_faculty", "test_group")
        self.assertEqual(tag, "dcc7ca1233b33ac0429f0c0aa1fce4")

    def test_add_lesson(self):
        tag = "dcc7ca1233b33ac0429f0c0aa1fce4"
        day = "Monday"
        number = 1
        week_type = 2
        time_start = "08:30"
        time_end = "09:30"
        title = "test_title"
        classroom = "test_classroom"
        lecturer = "test_lecturer"
        self.assertTrue(self.db.add_lesson(
            tag, day, number, week_type, time_start, time_end, title, classroom, lecturer))

    def test_add_report(self):
        cid = 111111111
        report = "test report"
        self.assertTrue(self.db.add_report(cid, report))

    def test_add_user(self):
        cid = 111111111
        name = "test_user"
        username = "test_username"
        tag = "dcc7ca1233b33ac0429f0c0aa1fce4"

        self.assertTrue(self.db.add_user(cid, name, username, tag))

    def test_update_user(self):
        cid = 111111111
        name = "test_user_updated"
        username = "test_username_updated"
        tag = "dcc7ca1233b33ac0429f0c0aa1fce4"

        self.assertTrue(self.db.update_user(cid, name, username, tag))

    def test_find_user(self):
        user_data = [222222222, "find_user_name", "find_user_username", "dcc7ca1233b33ac0429f0c0aa1fce4"]
        self.db.add_user(user_data[0], user_data[1], user_data[2], user_data[3])

        user = self.db.find_user(user_data[0])
        self.assertEqual((user_data[3],), user)

    def test_set_auto_post_time(self):
        user_data = [333333333, "auto_post_user_name", "auto_post_username", "dcc7ca1233b33ac0429f0c0aa1fce4"]
        self.db.add_user(user_data[0], user_data[1], user_data[2], user_data[3])

        self.assertTrue(self.db.set_auto_post_time(user_data[0], "08:30:00", True))

    def test_find_users_where(self):
        user_data = [[444444444, "name_1", "username_1", "dcc7ca1233b33ac0429f0c0aa1fce4"],
                     [555555555, "name_2", "username_2", "dcc7ca1233b33ac0429f0c0aa1fce4"],
                     [666666666, "name_3", "username_3", "dcc7ca1233b33ac0429f0c0aa1fce4"]]

        self.db.add_user(user_data[0][0], user_data[0][1], user_data[0][2], user_data[0][3])
        self.db.add_user(user_data[1][0], user_data[1][1], user_data[1][2], user_data[1][3])
        self.db.add_user(user_data[2][0], user_data[2][1], user_data[2][2], user_data[2][3])

        self.assertTrue(self.db.set_auto_post_time(user_data[0][0], "08:30:00", False))
        self.assertTrue(self.db.set_auto_post_time(user_data[1][0], "08:30:00", True))
        self.assertTrue(self.db.set_auto_post_time(user_data[2][0], "09:30:00", False))

        users = self.db.find_users_where(auto_posting_time="08:30:00")
        self.assertEqual([(user_data[0][0], user_data[0][3]), (user_data[1][0], user_data[1][3])], users)

    def test_get_schedule_all_week_types(self):
        real_data = [(1, 'ma_lesson_1'.ljust(100), 'cr_401'.ljust(20), 2),
                     (2, 'mo_lesson_2'.ljust(100), 'cr_402'.ljust(20), 0),
                     (2, 'me_lesson_2'.ljust(100), 'cr_403'.ljust(20), 1),
                     (3, 'ma_lesson_3'.ljust(100), 'cr_404'.ljust(20), 2)]

        tag = "test_tag_all_week_types"
        self.db.add_lesson(tag, "Monday", 1, 2, "08:30", "09:30", "ma_lesson_1", "cr_401", "lect_1")
        self.db.add_lesson(tag, "Monday", 2, 0, "09:30", "10:30", "mo_lesson_2", "cr_402", "lect_2_odd")
        self.db.add_lesson(tag, "Monday", 2, 1, "09:30", "10:30", "me_lesson_2", "cr_403", "lect_2_even")
        self.db.add_lesson(tag, "Monday", 3, 2, "10:30", "11:30", "ma_lesson_3", "cr_404", "lect_3")
        self.db.add_lesson(tag, "Tuesday", 1, 2, "08:30", "09:30", "ta_lesson_1", "cr_501", "lect_4")

        data = self.db.get_schedule(tag, "Monday")

        self.assertEqual(real_data, data)

    def test_get_schedule_odd_week_type(self):
        real_data = [(1, 'ma_lesson_1'.ljust(100), 'cr_401'.ljust(20), 2),
                     (2, 'mo_lesson_2'.ljust(100), 'cr_402'.ljust(20), 0),
                     (3, 'ma_lesson_3'.ljust(100), 'cr_404'.ljust(20), 2)]

        tag = "test_tag_odd_week_type"
        self.db.add_lesson(tag, "Monday", 1, 2, "08:30", "09:30", "ma_lesson_1", "cr_401", "lect_1")
        self.db.add_lesson(tag, "Monday", 2, 0, "09:30", "10:30", "mo_lesson_2", "cr_402", "lect_2_odd")
        self.db.add_lesson(tag, "Monday", 2, 1, "09:30", "10:30", "me_lesson_2", "cr_403", "lect_2_even")
        self.db.add_lesson(tag, "Monday", 3, 2, "10:30", "11:30", "ma_lesson_3", "cr_404", "lect_3")
        self.db.add_lesson(tag, "Tuesday", 1, 2, "08:30", "09:30", "ta_lesson_1", "cr_501", "lect_4")

        data = self.db.get_schedule(tag, "Monday", 0)

        self.assertEqual(real_data, data)

    def test_get_schedule_even_week_type(self):
        real_data = [(1, 'ma_lesson_1'.ljust(100), 'cr_401'.ljust(20), 2),
                     (2, 'me_lesson_2'.ljust(100), 'cr_403'.ljust(20), 1),
                     (3, 'ma_lesson_3'.ljust(100), 'cr_404'.ljust(20), 2)]

        tag = "test_tag_even_week_type"
        self.db.add_lesson(tag, "Monday", 1, 2, "08:30", "09:30", "ma_lesson_1", "cr_401", "lect_1")
        self.db.add_lesson(tag, "Monday", 2, 0, "09:30", "10:30", "mo_lesson_2", "cr_402", "lect_2_odd")
        self.db.add_lesson(tag, "Monday", 2, 1, "09:30", "10:30", "me_lesson_2", "cr_403", "lect_2_even")
        self.db.add_lesson(tag, "Monday", 3, 2, "10:30", "11:30", "ma_lesson_3", "cr_404", "lect_3")
        self.db.add_lesson(tag, "Tuesday", 1, 2, "08:30", "09:30", "ta_lesson_1", "cr_501", "lect_4")

        data = self.db.get_schedule(tag, "Monday", 1)

        self.assertEqual(real_data, data)

    def test_get_organizations(self):
        self.maxDiff = None

        real_organizations = [('test_organization_01'.ljust(80), '1b110c6f26d3dd30429f0c0aa62028'),
                              ('test_organization_02'.ljust(80), '86de8e25b7f22ce0429f0c0aa62028'),
                              ('test_organization_03'.ljust(80), '2e93e910b8dde740429f0c0aa7d7d9')]

        self.db.add_organization("test_organization_01", "test_faculty", "test_group_1")
        self.db.add_organization("test_organization_01", "test_faculty", "test_group_2")

        self.db.add_organization("test_organization_02", "test_faculty", "test_group_1")
        self.db.add_organization("test_organization_02", "test_faculty", "test_group_2")

        self.db.add_organization("test_organization_03", "test_faculty", "test_group_1")

        organizations = self.db.get_organizations()
        self.assertEqual(organizations, real_organizations)

    def test_get_faculty(self):
        real_faculty = [('test_faculty_11'.ljust(80), '07039519f908f09072827d0ed7d7d9'),
                        ('test_faculty_12'.ljust(80), '07039519f908f09f4a63a885d62028')]

        tag = self.db.add_organization("test_organization_11", "test_faculty_11", "test_group_1")
        self.db.add_organization("test_organization_11", "test_faculty_12", "test_group_2")

        self.db.add_organization("test_organization_12", "test_faculty_21", "test_group_1")
        self.db.add_organization("test_organization_12", "test_faculty_22", "test_group_2")

        self.db.add_organization("test_organization_13", "test_faculty_31", "test_group_1")

        faculty = self.db.get_faculty(tag[:scheduledb.organization_field_length])
        self.assertEqual(faculty, real_faculty)

    def test_get_group(self):
        real_groups = [('test_group_1'.ljust(20), 'dcbd54fa7339d17072827d0ed7d7d9'),
                       ('test_group_2'.ljust(20), 'dcbd54fa7339d17072827d0ed62028')]

        tag = self.db.add_organization("test_organization_21", "test_faculty_11", "test_group_1")
        self.db.add_organization("test_organization_21", "test_faculty_11", "test_group_2")
        self.db.add_organization("test_organization_21", "test_faculty_12", "test_group_2")

        self.db.add_organization("test_organization_22", "test_faculty_21", "test_group_1")
        self.db.add_organization("test_organization_22", "test_faculty_22", "test_group_2")

        self.db.add_organization("test_organization_23", "test_faculty_31", "test_group_1")

        groups = self.db.get_group(tag[:scheduledb.organization_field_length + scheduledb.faculty_field_length])
        self.assertEqual(groups, real_groups)


if __name__ == '__main__':
    unittest.main()