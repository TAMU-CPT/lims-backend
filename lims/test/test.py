from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time


class UserTestCase(LiveServerTestCase):

    @classmethod  # called only once before all tests
    def setUpClass(cls):
        print "Tests starting"
        user = User.objects.create_user('foo', password='bar')
        user.save()
        cls.driver = webdriver.Chrome()
        super(UserTestCase, cls).setUpClass()

    def test_A_then_B(self):
        self.login()
        self.env_sample_create()

    def login(self):
        driver = self.driver
        driver.get("http://localhost:10000/#/login")
        login_button = driver.find_element_by_xpath("//md-card-content/button")
        username = driver.find_element_by_name('name')
        password = driver.find_element_by_name('password')
        username.send_keys("foo")  # set up above
        password.send_keys("bar")  # set up above
        time.sleep(2)
        print User.objects.all()
        login_button.click()
        print User.objects.all()
        time.sleep(2)

    def env_sample_create(self):
        print User.objects.all()
        driver = self.driver
        driver.get("http://localhost:10000/#/environmentalsamples")
        time.sleep(2)
        driver.find_element_by_xpath("//button[@aria-label='Register a New Environmental Sample']").click()
        time.sleep(2)

    @classmethod  # called once after all tests are finished
    def tearDownClass(cls):
        print "Tests ending"
        cls.driver.close()
        super(UserTestCase, cls).tearDownClass()
