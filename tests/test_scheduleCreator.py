import sys
import unittest

sys.path.append('../')

from config import config
import scheduleCreator
import scheduledb


class TestScheduleCreator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with scheduledb.ScheduleDB(config) as db:
            cls.tag = db.add_organization('test_organization', 'test_faculty', 'test_group')
            db.add_lesson(cls.tag, "Monday", 1, 2, "08:30", "09:30", "ma_lesson_1", "cr_401", "lect_1")
            db.add_lesson(cls.tag, "Monday", 2, 0, "09:30", "10:30", "mo_lesson_2", "cr_402", "lect_2_odd")
            db.add_lesson(cls.tag, "Monday", 2, 1, "09:30", "10:30", "me_lesson_2", "cr_403", "lect_2_even")
            db.add_lesson(cls.tag, "Monday", 3, 2, "10:30", "11:30", "ma_lesson_3", "cr_404", "lect_3")
            db.add_lesson(cls.tag, "Tuesday", 1, 2, "08:30", "09:30", "ta_lesson_1", "cr_501", "lect_4")

    @classmethod
    def tearDownClass(cls):
        with scheduledb.ScheduleDB(config) as db:
            db.clear_tables()

    def test_create_schedule_text_all_week_types(self):
        real_schedule = ['>Понедельник:\n1 пара:\nma_lesson_1 cr_401 \n------------\n' +
                         '2 пара:\nmo_lesson_2 cr_402 числ\nme_lesson_2 cr_403 знам\n------------\n' +
                         '3 пара:\nma_lesson_3 cr_404 \n------------\n']
        schedule = scheduleCreator.create_schedule_text(self.tag, "Monday")
        self.assertEqual(schedule, real_schedule)

    def test_create_schedule_text_odd_week(self):
        real_schedule = ['>Понедельник:\n1 пара:\nma_lesson_1 cr_401 \n------------\n' +
                         '2 пара:\nmo_lesson_2 cr_402 \n------------\n' +
                         '3 пара:\nma_lesson_3 cr_404 \n------------\n']
        schedule = scheduleCreator.create_schedule_text(self.tag, "Monday", 0)
        self.assertEqual(schedule, real_schedule)

    def test_create_schedule_text_even_week(self):
        real_schedule = ['>Понедельник:\n1 пара:\nma_lesson_1 cr_401 \n------------\n' +
                         '2 пара:\nme_lesson_2 cr_403 \n------------\n' +
                         '3 пара:\nma_lesson_3 cr_404 \n------------\n']
        schedule = scheduleCreator.create_schedule_text(self.tag, "Monday", 1)
        self.assertEqual(schedule, real_schedule)

if __name__ == '__main__':
    unittest.main()