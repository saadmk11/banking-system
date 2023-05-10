from seleniumbase import BaseCase
from my_test_suite import MyTestSuite


class MyOtherTestSuite(BaseCase):

    def test_1(self):
        # Import the MyTestSuite class from my_test_suite.py
        my_test_suite = MyTestSuite(self.driver)
        # Run the first test case from MyTestSuite
        my_test_suite.test_1()

    def test_2(self):
        # Import the MyTestSuite class from my_test_suite.py
        my_test_suite = MyTestSuite(self.driver)
        # Run the second test case from MyTestSuite
        my_test_suite.test_2()

    def test_3(self):
        # Import the MyTestSuite class from my_test_suite.py
        my_test_suite = MyTestSuite(self.driver)
        # Run the third test case from MyTestSuite
        my_test_suite.test_3()

    def test_4(self):
        # Import the MyTestSuite class from my_test_suite.py
        my_test_suite = MyTestSuite(self.driver)
        # Run the fourth test case from MyTestSuite
        my_test_suite.test_4()