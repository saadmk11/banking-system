from seleniumbase import BaseCase
import pytest
import logging

class BaseLoginTest(BaseCase):
    def setUp(self):
        self.driver_name = "Chrome"
        super().setUp()
        # <<< Run custom setUp() code for tests AFTER the super().setUp() >>>

    def tearDown(self):
        self.save_teardown_screenshot()  # On failure or "--screenshot"
        if self.has_exception():
            # <<< Run custom code if the test failed. >>>
            pass
        else:
            # <<< Run custom code if the test passed. >>>
            pass
        # (Wrap unreliable tearDown() code in a try/except block.)
        # <<< Run custom tearDown() code BEFORE the super().tearDown() >>>
        super().tearDown()
        
    @pytest.mark.jira('AT-1')
    def login(self, username, password):
        # <<< Placeholder. Add your code here. >>>
        # Reduce duplicate code in tests by having reusable methods like this.
        # If the UI changes, the fix can be applied in one place.
        self.open("http://localhost:8001/")
        self.click('a[href="/accounts/login/"]')
        self.open_if_not_url("http://localhost:8001/accounts/login/")
        self.click("body.bg-gray-100 div form div")
        self.type("input#id_username", username)
        self.type("input#id_password", password)
        self.click('button:contains("Sign In")')
    
    def logout(self):
        self.assert_exact_text("Logout", 'a[href="/accounts/logout/"]')
        self.click('a[href="/accounts/logout/"]')
        self.assert_exact_text("Login", 'a[href="/accounts/login/"]')

    def assert_login_success(self, elem):
        # Check that the login was successful
        self.assert_element(elem)

    def assert_login_failure(self, elem):
        # Check that the login failed
        self.assert_element(elem)

    def assert_login_fail_show_require_username(self, elem):
        # Check that when login with empty username, it shows error message on the correct place
        self.assert_element(elem)
    
    def assert_login_fail_show_require_password(self, elem):
        # Check that when login with empty username, it shows error message on the correct place
        self.assert_element(elem)
        
        
        
class TestValidLogin(BaseLoginTest):
    @pytest.mark.jira('AT-5')
    def test_login_with_valid_credentials(self):
        # Perform the valid login test
        logging.info("Test valid login with valid credentials")
        self.login("uarehup@gmail.com", "user123456")
        self.assert_login_success('a[href="/accounts/logout/"]')

class TestInvalidLogin(BaseLoginTest):
    @pytest.mark.jira('AT-6')
    def test_login_with_invalid_credentials(self):
        # Perform the invalid login test
        logging.info("Test invalid login with invalid credentials")
        self.login("uarehup@gmail.com", "user123")
        self.assert_login_failure("body > div > div.bg-red-100.border.border-red-400.text-red-700.px-4.py-3.rounded.relative.mt-2")
        
    def test_login_with_empty_username(self):
        # Perform the invalid login test without username
        logging.info("Test invalid login test without username")
        self.login("", "user123")
        self.assert_login_fail_show_require_username("body > div > div > form > p:nth-child(3)")
        
    def test_login_with_empty_password(self):        
        # Perform the invalid login test without password
        logging.info("Test invalid login test without password")
        self.login("", "user123")
        self.assert_login_fail_show_require_password("body > div > div > form > p:nth-child(5)")