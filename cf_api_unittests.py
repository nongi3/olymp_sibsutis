import datetime
import time
import unittest
import urllib.request

try:
    from . import cf_api, constants
except ImportError:
    import cf_api
    import constants


class TestCfApi(unittest.TestCase):

    def test_count_of_points_for_a_task_with_rating(self):
        self.assertEqual(cf_api.countOfPointsForATaskWithRating(constants.wrong_handle, 1000), 6.0)
        self.assertEqual(cf_api.countOfPointsForATaskWithRating(constants.correct_handle, 1000), 0)
        self.assertEqual(cf_api.countOfPointsForATaskWithRating(constants.correct_handle, 1010), 0)
        self.assertTrue(cf_api.countOfPointsForATaskWithRating(constants.correct_handle, 1800) > 0)

    def test_count_of_task_with_rating(self):
        current_count_of_task_with_2000 = 21        # was updated 18.03.2020
        self.assertEqual(cf_api.countOfTasksWithRating(constants.wrong_handle, 1000), 0)
        self.assertEqual(cf_api.countOfTasksWithRating(constants.correct_handle, 1010), 0)
        self.assertEqual(cf_api.countOfTasksWithRating(constants.correct_handle, 3000), 0)
        self.assertEqual(cf_api.countOfTasksWithRating(constants.correct_handle, 2000), current_count_of_task_with_2000)

    def test_finding_codeforces_points(self):
        self.assertEqual(-1, cf_api.findCodeforcesPoints(constants.wrong_handle))
        current_count_of_points = 5571  # was updated 17.03.2020
        self.assertTrue(current_count_of_points <= cf_api.findCodeforcesPoints(constants.correct_handle))

    def test_finding_gym_points(self):
        self.assertEqual(-1, cf_api.findGymPoints(constants.wrong_handle))
        current_count_of_points = 324  # was updated 17.03.2020
        self.assertTrue(current_count_of_points <= cf_api.findGymPoints(constants.correct_handle))

    def test_for_relevant(self):
        self.assertFalse(cf_api.isStillRelevant(constants.correct_handle, 1000))
        self.assertTrue(cf_api.isStillRelevant(constants.correct_handle, 1800))
        self.assertTrue(cf_api.isStillRelevant(constants.wrong_handle, 1800))

    def test_getting_all_unsolved_task(self):
        self.assertEqual(cf_api.getInfoAboutSolvedTasksWithHandle('ruban'), cf_api.getAllUnsolvedTasks())

    def test_getting_count_of_rating_contest_from_time(self):
        self.assertTrue('Error' in cf_api.getCountOfRatedContestFromTime(constants.wrong_handle, 0))
        current_time = time.mktime(datetime.datetime.now().timetuple())
        self.assertEqual(cf_api.getCountOfRatedContestFromTime(constants.correct_handle, current_time + 5), 0)
        current_count_of_rating_contest = 74        # was updated 18.03.2020
        self.assertEqual(cf_api.getCountOfRatedContestFromTime(constants.correct_handle, 0),
                         current_count_of_rating_contest)

    def test_getting_count_of_solved_task_with_contest_id(self):
        self.assertEqual(cf_api.getCountOfSolvedTaskWithContestId('100135', constants.correct_handle), 6)
        self.assertEqual(cf_api.getCountOfSolvedTaskWithContestId('-124', constants.correct_handle), -1)
        self.assertEqual(cf_api.getCountOfSolvedTaskWithContestId('abc3a', constants.correct_handle), -1)
        self.assertEqual(cf_api.getCountOfSolvedTaskWithContestId('100135', constants.wrong_handle), -1)
        self.assertEqual(cf_api.getCountOfSolvedTaskWithContestId('-124', constants.wrong_handle), -1)
        self.assertEqual(cf_api.getCountOfSolvedTaskWithContestId('abc3a', constants.wrong_handle), -1)

    def test_getting_count_of_submissions_for_a_month(self):
        self.assertTrue('Error' in cf_api.getCountOfSubmissionsForAMonth(constants.wrong_handle))
        self.assertEqual(0, cf_api.getCountOfSubmissionsForAMonth('Tornem'))
        self.assertTrue(cf_api.getCountOfSubmissionsForAMonth(constants.correct_handle) > 0)

    def test_getting_info_about_solved_tasks(self):
        self.assertTrue('Error' in cf_api.getInfoAboutSolvedTasksWithHandle(constants.wrong_handle))
        getting_result = cf_api.getInfoAboutSolvedTasksWithHandle(constants.correct_handle)
        self.assertFalse('Error' in getting_result)

    def test_getting_set_of_unsolved_tasks(self):
        self.assertEqual(cf_api.getSetOfHundredTasks(constants.wrong_handle, 10, 1000), [])
        self.assertEqual(len(cf_api.getSetOfHundredTasks(constants.correct_handle, 10, 2000)), 10)
        self.assertEqual(len(cf_api.getSetOfHundredTasks(constants.correct_handle, 10, 500)), 0)

    def test_getting_task_with_tag_and_rating(self):
        self.assertTrue('Error' in cf_api.getTaskWithTagAndRating(constants.wrong_handle, '', '1000'))
        self.assertTrue('Error' in cf_api.getTaskWithTagAndRating(constants.correct_handle, '', '1010'))
        self.assertEqual(200, urllib.request.urlopen(
            cf_api.getTaskWithTagAndRating(constants.correct_handle, '', 1900)).getcode())
        self.assertEqual(200, urllib.request.urlopen(
            cf_api.getTaskWithTagAndRating(constants.correct_handle, 'greedy;graphs', 1900)).getcode())

    def test_getting_time_for_last_submission(self):
        self.assertEqual(0, cf_api.getTimeOfLastSubmissionWithHandle(constants.wrong_handle))

    def test_getting_unsolved_tasks_with_handle(self):
        self.assertTrue(cf_api.getUnsolvedTasksWithHandle('ruban') == {})
        self.assertTrue(cf_api.getUnsolvedTasksWithHandle(constants.wrong_handle) == {})
        self.assertTrue(len(cf_api.getUnsolvedTasksWithHandle(constants.correct_handle)) > 0)

    def test_getting_vk_id_from_cf(self):
        vk_id_of_correct_handle = '30806644'
        self.assertEqual(vk_id_of_correct_handle, cf_api.getVkIdFromCodeforces(constants.correct_handle))
        self.assertEqual('Error', cf_api.getVkIdFromCodeforces(constants.wrong_handle))
