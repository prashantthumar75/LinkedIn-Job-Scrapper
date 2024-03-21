from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import json



class JobSearch:

    def __init__(self, data):
        """Parameter initialization"""

        self.email = data['email']
        self.password = data['password']
        self.keyword = data['keyword']
        self.options = Options()
        self.driver = webdriver.Chrome(options=self.options)
        self.applications = []

    def login_linkedin(self):
        """Login to LinkedIn"""

        # Go to the LinkedIn login URL
        self.driver.get("https://www.linkedin.com/login")
        try:
            # Input email and password then press enter
            login_email = self.driver.find_element(By.ID, "username")
            login_email.clear()
            login_email.send_keys(self.email)
            login_pass = self.driver.find_element(By.ID, "password")
            login_pass.clear()
            login_pass.send_keys(self.password)
            login_pass.send_keys(Keys.RETURN)
            self.driver.get("https://www.linkedin.com/jobs")

        except:
            login_pass = self.driver.find_element(By.ID, "password")
            login_pass.clear()
            login_pass.send_keys(self.password)
            login_pass.send_keys(Keys.RETURN)
            self.driver.get("https://www.linkedin.com/jobs")

    def search_jobs(self):
        """Search for jobs"""

        # Click and input keywords in the search box
        keyword_search_box = self.driver.find_element(By.XPATH, "//*[contains(@id, 'jobs-search-box-keyword-id')]")
        keyword_search_box.click()
        keyword_search_box.send_keys(self.keyword)
        keyword_search_box.send_keys(Keys.RETURN)

    def apply_filters(self):
        """Apply filters to job search results"""

        time.sleep(5)
        parent_element = self.driver.find_element(By.CLASS_NAME, "scaffold-layout__list-container")
        time.sleep(2)
        child_elements = parent_element.find_elements(By.CLASS_NAME, "scaffold-layout__list-item")
        for child in child_elements:
            try:
                job_card_container = child.find_element(By.CLASS_NAME, "job-card-container")
                apply_method_div = job_card_container.find_element(By.CLASS_NAME, "job-card-container__apply-method")
            except NoSuchElementException:
                child.click()
                time.sleep(3)
                job_title_span = self.driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__job-title-link")
                job_title = job_title_span.get_attribute("innerHTML")
                job_description_span = self.driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__primary-description-without-tagline")
                job_description = job_description_span.get_attribute("innerHTML")

                try:
                    self.driver.find_element(By.CLASS_NAME, "jobs-apply-button").click()
                    new_tab = self.driver.window_handles[-1]
                    self.driver.switch_to.window(new_tab)
                    data = {
                        "URL": self.driver.current_url,
                        "Job Title": job_title,
                        "Job Description": job_description
                    }

                    self.applications.append(data)
                    old_tab = self.driver.window_handles[0]
                    self.driver.close()
                    self.driver.switch_to.window(old_tab)
                    print(data)

                    with open('job_applications.json', 'a') as json_file:
                        json.dump(self.applications, json_file)

                except NoSuchElementException:
                    print("No link")

    def close_session(self):
        """Close the browser session"""

        print('End of the session, see you later!')
        self.driver.close()

    def apply_to_jobs(self):
        """Apply to job offers"""

        self.driver.maximize_window()
        try:
            self.login_linkedin()
        except:
            self.driver.get("https://www.linkedin.com/jobs/")
        time.sleep(5)
        self.search_jobs()
        time.sleep(10)
        self.apply_filters()
        self.close_session()

if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)

    bot = JobSearch(data)
    bot.apply_to_jobs()
