from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class RecorderTest(BaseCase):
    def test_recording(self):
        self.open("http://localhost:8001/")
        self.click('a[href="/accounts/login/"]')
        self.open_if_not_url("http://localhost:8001/accounts/login/")
        self.click("body.bg-gray-100 div form div")
        self.type("input#id_username", "uarehup@gmail.com")
        self.type("input#id_password", "user123456")
        self.click('button:contains("Sign In")')
        self.open_if_not_url("http://localhost:8001/")
        self.click('a[href="/accounts/logout/"]')
        self.open_if_not_url("http://localhost:8001/")
