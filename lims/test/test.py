from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time


class UserTestCase(LiveServerTestCase):

    @classmethod  # called only once before all tests
    def setUpClass(cls):
        print "class starting"
        user = User.objects.create_user('foo', password='bar')
        user.save()
        cls.driver = webdriver.Chrome()
        super(UserTestCase, cls).setUpClass()

    def test_login(self):
        driver = self.driver
        driver.get("http://localhost:10000/#/login")
        login_button = driver.find_element_by_xpath("//md-card-content/button")
        username = driver.find_element_by_xpath("//input[@name='name']")
        password = driver.find_element_by_xpath("//input[@name='password']")
        username.send_keys("foo")  # set up above
        password.send_keys("bar")  # set up above
        login_button.click()
        time.sleep(2)

    @classmethod  # called once after all tests are finished
    def tearDownClass(cls):
        print "class ending"
        cls.driver.close()
        super(UserTestCase, cls).tearDownClass()
