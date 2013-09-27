import os

from selenium.webdriver.support.wait import WebDriverWait

from django.core.urlresolvers import reverse
from django.test import LiveServerTestCase
from django.utils.unittest import SkipTest

from myanalytics.models import SiteView, SiteViewer, UserAgent
from myjobs.tests.factories import UserFactory


class MyAnalyticsCombinedTests(LiveServerTestCase):
    urls = 'MyJobs.myanalytics.test_urls'

    def login(self, username, password):
        self.selenium.get(self.live_server_url)
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        username_field = self.selenium.find_element_by_xpath(
            '//input[@id="id_username"]')
        username_field.send_keys(username)
        password_field = self.selenium.find_element_by_xpath(
            '//input[@id="id_password"]')
        password_field.send_keys(password)
        self.selenium.find_element_by_id('login').click()

    @classmethod
    def setUpClass(cls):
        if not os.environ.get('DJANGO_SELENIUM_TESTS', False):
            raise SkipTest('Selenium tests not requested')

        try:
            from selenium.webdriver.firefox.webdriver import WebDriver
        except ImportError as e:
            raise SkipTest('Selenium webdriver is not installed or not '
                           'operational: %s' % (str(e)))
        cls.selenium = WebDriver()
        cls.selenium.delete_all_cookies()
        super(MyAnalyticsCombinedTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.delete_all_cookies()
        cls.selenium.quit()
        super(MyAnalyticsCombinedTests, cls).tearDownClass()

    def setUp(self):
        self.user = UserFactory()

    def test_add_correct_viewer_type(self):
        """
        Tracking a view should correctly determine the user based on who is
        currently logged into My.jobs. This can be improved once external
        access to My.jobs accounts has been implemented.
        """
        # Non-authenticated
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('analytics_test')))
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.assertEqual(SiteViewer.objects.count(), 1)
        self.assertEqual(SiteView.objects.count(), 1)
        self.assertEqual(UserAgent.objects.count(), 1)

        # A non-authenticated viewer should have the user field on their
        # session log set to None
        viewer = SiteViewer.objects.all()[0]
        self.assertEqual(viewer.user, None)

        # Authenticated
        self.login(self.user.email, 'secret')
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('analytics_test')))
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.assertEqual(SiteViewer.objects.count(), 2)
        self.assertEqual(SiteView.objects.count(), 2)
        self.assertEqual(UserAgent.objects.count(), 1)

        # An authenticated viewer should have the user field on their session
        # log set to their user instance
        viewer = SiteViewer.objects.all()[1]
        self.assertEqual(viewer.user, self.user)

    def test_anonymous_id_generation(self):
        """
        Currently, a new ID is only generated if cookies are cleared or the
        viewer is using a new device. This can be improved once facilities
        are in place for allowing access to My.jobs account information
        externally.
        """
        self.login(self.user.email, 'secret')

        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('analytics_test')))
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('analytics_test')))
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.assertEqual(SiteViewer.objects.count(), 1)
        self.assertEqual(SiteView.objects.count(), 2)

        self.selenium.delete_all_cookies()

        self.login(self.user.email, 'secret')
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('analytics_test')))
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        self.assertEqual(SiteViewer.objects.count(), 2)
        self.assertEqual(SiteView.objects.count(), 3)

        viewers = SiteViewer.objects.all()
        self.assertNotEqual(viewers[0].aguid, viewers[1].aguid)
        self.assertEqual(viewers[0].user, viewers[1].user)

    def test_share_clicks(self):
        """
        Clicking on a share button should track which button was clicked.
        """
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('analytics_test')))
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.selenium.find_elements_by_class_name('at15nc')[0].click()
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.execute_script('return document.readyState == "complete"'))

        self.assertEqual(SiteView.objects.count(), 2)
        view = SiteView.objects.all()[1]
        self.assertEqual(view.goal, 'share')
        self.assertEqual(view.share_site, 'Twitter')

        self.selenium.find_elements_by_class_name('at16nc')[0].click()
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.execute_script('return document.readyState == "complete"'))

        self.assertEqual(SiteView.objects.count(), 3)
        view = SiteView.objects.all()[2]
        self.assertEqual(view.goal, 'share')
        self.assertEqual(view.share_site, 'Facebook')

    def test_apply_click(self):
        """
        Clicking on an apply button tracks that the button was clicked as well
        as what the button was pointing to.
        """
        self.selenium.get('%s%s' % (self.live_server_url,
                                    reverse('analytics_test')))
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.find_element_by_tag_name('body'))
        self.selenium.find_element_by_id('direct_applyButton').click()
        WebDriverWait(self.selenium, 5).until(
            lambda driver: driver.execute_script('return document.readyState == "complete"'))

        self.assertEqual(SiteView.objects.count(), 2)
        view = SiteView.objects.all()[1]
        self.assertEqual(view.goal, 'apply')
        self.assertEqual(view.goal_url, 'http://example.com/apply_here')
