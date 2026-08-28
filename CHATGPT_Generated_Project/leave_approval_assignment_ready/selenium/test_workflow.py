import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL=os.getenv('BASE_URL','http://127.0.0.1:8000')

class DashboardSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options=Options(); options.add_argument('--headless'); options.add_argument('--no-sandbox'); options.add_argument('--disable-dev-shm-usage')
        cls.driver=webdriver.Chrome(options=options)
    @classmethod
    def tearDownClass(cls): cls.driver.quit()
    def test_dashboard_loads(self):
        self.driver.get(BASE_URL+'/dashboard')
        self.assertIn('Employee Leave Approval System', self.driver.title)
        self.assertIn('Admin Oversight Dashboard', self.driver.find_element(By.ID,'status').text)

if __name__=='__main__': unittest.main()
