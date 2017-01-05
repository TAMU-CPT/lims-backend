from django.test import TestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('foo', password='bar')
        user.save()
        self.driver = webdriver.Chrome()

    def test_login(self):
        driver = self.driver
        driver.get("http://localhost:10000/#/login")
        login_button = driver.find_element_by_xpath("//md-card-content/button")
        username = driver.find_element_by_xpath("//input[@name='name']")
        password = driver.find_element_by_xpath("//input[@name='password']")
        username.send_keys("foo") # set up above
        password.send_keys("bar") # set up above
        login_button.click()
        time.sleep(5)
