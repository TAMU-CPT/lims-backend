from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import time


class UserTestCase(LiveServerTestCase):

    @classmethod  # called only once before all tests
    def setUpClass(cls):
        super(UserTestCase, cls).setUpClass()
        user = User.objects.create_user('foo', password='bar')
        user.save()
        cls.driver = webdriver.Chrome()

    def test_A_then_B(self):
        print self.live_server_url
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
        time.sleep(0.2)
        login_button.click()
        driver.save_screenshot('media/after_login.png')
        time.sleep(2)

    def env_sample_create(self):
        driver = self.driver
        driver.find_element_by_xpath("//a[@aria-label='Environmental Samples']").click()
        driver.find_element_by_xpath("//button[@aria-label='Register a New Environmental Sample']").click()
        time.sleep(2)
        driver.find_element_by_name("sample_type").send_keys("sewage")
        driver.find_element_by_name("description").send_keys("waste facility in Bryan")
        driver.find_element_by_name("room").send_keys("312")
        driver.find_element_by_name("storage_type").click()
        driver.find_element_by_xpath("//md-option[2]").click()
        driver.find_element_by_name("container_label").send_keys("312 F1")
        driver.find_element_by_name("shelf").send_keys("1")
        driver.find_element_by_name("box_label").send_keys("464 env samples")
        driver.find_element_by_name("tube").send_keys("env sample 1")
        time.sleep(3)
        driver.find_element_by_xpath("//button[@aria-label='Create']").click()
        time.sleep(2)
        driver.find_element_by_partial_link_text("LIMS").click()
        driver.find_element_by_xpath("//a[@aria-label='Environmental Samples']").click()  # lets you see that the object is in the table. need to assert this somehow
        time.sleep(2)
        print(driver.page_source)
        time.sleep(2)

    @classmethod  # called once after all tests are finished
    def tearDownClass(cls):
        cls.driver.quit()
        super(UserTestCase, cls).tearDownClass()
        print 'done'
