import json
import unittest
import pandas as pd

from app import webserver
from app import routes

class Test(unittest.TestCase):
    # read the data from the read.csv file
    def setUp(self):
        self.data = pd.read_csv('nutrition_activity_obesity_usa_subset.csv')
    
    def test_get_req_for_server_shutdown(self):
        # check if the server is up
        webserver.test_client().get('api/graceful_shutdown')
        res = webserver.test_client().get('api/jobs')
        self.assertEqual(res.status_code, 200)

    def test_post_req_for_states_mean(self):
        webserver.test_client().get('api/graceful_shutdown')
        res = webserver.test_client().post('/api/states_mean', json={"question": self.data['Question'].iloc[0]})
        # expected to get a 500 status code as the server is shutdown
        self.assertEqual(res.status_code, 500)

    def test_api_states_mean(self):
        # use the function from routes to the the states mean and take the data from in-1.json
        with open ('./tests/states_mean/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_states_mean(data)

        # check if the response is in the out directory
        with open('./tests/states_mean/output/out-1.json') as f:
            expected = json.load(f)

        self.assertEqual(res, expected)

    def test_api_states_mean_fail(self):
        data = {'question' : 'Fake question'}

        res = routes.api_states_mean(data)

        # Check if the response is in the out directory
        with open('./tests/states_mean/output/out-1.json') as f:
            expected = json.load(f)

        self.assertNotEqual(res, expected)  # This should cause the test to fail

    def test_api_state_mean(self):
        # use the function from routes to the the states mean and take the data from in-1.json
        with open ('./tests/state_mean/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_state_mean(data)

        # check if the response is in the out directory
        with open('./tests/state_mean/output/out-1.json') as f:
            expected = json.load(f)

        self.assertEqual(res, expected)

    def test_api_state_mean_fail(self):
        data = {'question' : 'Percent of adults aged 18 years and older who have an overweight classification'}

        with self.assertRaises(KeyError):
            routes.api_state_mean(data)

    def test_api_best5(self):
        # use the function from routes to the the states mean and take the data from in-1.json
        with open ('./tests/best5/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_best5(data)

        # check if the response is in the out directory
        with open('./tests/best5/output/out-1.json') as f:
            expected = json.load(f)

        self.assertEqual(res, expected)

    def test_api_best5_fail(self):
        data = {'question' : 'Fake question'}

        res = routes.api_states_mean(data)

        # Check if the response is in the out directory
        with open('./tests/states_mean/output/out-1.json') as f:
            expected = json.load(f)

        self.assertNotEqual(res, expected)  # This should cause the test to fail

    def test_api_worst5(self):
        # use the function from routes to the the states mean and take the data from in-1.json
        with open ('./tests/worst5/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_worst5(data)

        # check if the response is in the out directory
        with open('./tests/worst5/output/out-1.json') as f:
            expected = json.load(f)

        self.assertEqual(res, expected)

    def test_api_worst5_fail(self):
        data = {'question' : 'Fake question'}

        res = routes.api_worst5(data)

        # Check if the response is in the out directory
        with open('./tests/worst5/output/out-1.json') as f:
            expected = json.load(f)

        self.assertNotEqual(res, expected)


    def test_global_mean(self):
        with open('./tests/global_mean/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_global_mean(data)

        with open('./tests/global_mean/output/out-1.json') as f:
            expected = json.load(f)

        # Define a margin of error (tolerance)
        margin_of_error = 0.00000000000001

        # Check if the difference between res and expected is within the margin of error
        for key in expected.keys():
            self.assertAlmostEqual(res[key], expected[key], delta=margin_of_error)
    

    def test_global_mean_fail(self):
        data = {'question' : 'Fake question'}

        res = routes.api_global_mean(data)

        with open('./tests/global_mean/output/out-1.json') as f:
            expected = json.load(f)

        self.assertNotEqual(res, expected)

    def test_diff_from_mean(self):
        with open('./tests/diff_from_mean/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_diff_from_mean(data)

        with open('./tests/diff_from_mean/output/out-1.json') as f:
            expected = json.load(f)

        # Set self.maxDiff to None to see the full difference in case of assertion failure
        tolerance = 0.00000000000001

        for key in expected:
            self.assertAlmostEqual(res[key], expected[key], delta=tolerance)

    def test_diff_from_mean_fail(self):
        data = {'question' : 'Fake question'}

        res = routes.api_diff_from_mean(data)

        with open('./tests/diff_from_mean/output/out-1.json') as f:
            expected = json.load(f)

        self.assertNotEqual(res, expected)

    def test_api_state_diff_from_mean(self):
        with open('./tests/state_diff_from_mean/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_state_diff_from_mean(data)

        with open('./tests/state_diff_from_mean/output/out-1.json') as f:
            expected = json.load(f)

        self.assertEqual(res, expected)

    def test_api_state_diff_from_mean_fail(self):
        data = {'question' : 'Percent of adults aged 18 years and older who have an overweight classification'}

        with self.assertRaises(KeyError):
            routes.api_state_diff_from_mean(data)

    def test_api_mean_by_category(self):
        with open('./tests/mean_by_category/input/in-1.json') as f:
            data = json.load(f)

        res = routes.api_mean_by_category(data)

        with open('./tests/mean_by_category/output/out-1.json') as f:
            expected = json.load(f)

        self.assertEqual(res, expected)


    def test_api_mean_by_category_fail(self):
        data = {'question' : 'Fake question'}

        res = routes.api_mean_by_category(data)

        with open('./tests/mean_by_category/output/out-1.json') as f:
            expected = json.load(f)

        self.assertNotEqual(res, expected)

    def test_api_state_mean_by_category_fail(self):
        data = {'state' : 'District of Columbia'}

        with self.assertRaises(KeyError):
            routes.api_state_mean_by_category(data)

if __name__ == '__main__':
    unittest.main()

