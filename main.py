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

        self.driver.maximize_window()
        try:
            self.login_linkedin()
        except:
            self.driver.get("https://www.linkedin.com/jobs/")

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
            # self.driver.get("https://www.linkedin.com/jobs")

        except Exception as e:
            print('e', e)
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

    def send_messages(self):
        """Search for jobs"""
        self.driver.get("https://www.linkedin.com/search/results/people/?network=%5B%22F%22%5D&origin=FACETED_SEARCH&sid=UcA")
        time.sleep(5)
        all_button = self.driver.find_elements(By.TAG_NAME, "button")
        msg_button = [btn for btn in all_button if btn.text == 'Message']
        for i in range(4, 5): #Prashant Patel
        # for i in range(2, len(msg_button)):
            self.driver.execute_script("arguments[0].click();", msg_button[i])
            time.sleep(2)
            main_div = self.driver.find_element(By.XPATH, "//div[starts-with(@class, 'msg-form__msg-content-container')]")
            self.driver.execute_script("arguments[0].click();", main_div)
            paragraphs = self.driver.find_elements(By.TAG_NAME, "p")
            paragraphs[-5].send_keys("Hii")
            time.sleep(2)
            submit = self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            time.sleep(5)

    def send_connection(self):
        """Search for jobs"""
        self.driver.get("https://www.linkedin.com/search/results/people/?origin=FACETED_SEARCH&sid=tbZ")
        time.sleep(5)
        all_button = self.driver.find_elements(By.TAG_NAME, "button")
        print('all_button', all_button)
        msg_button = [btn for btn in all_button if btn.text == 'Connect']
        for i in range(2, 10):
        # for i in range(2, len(msg_button)):
            self.driver.execute_script("arguments[0].click();", msg_button[i])
            time.sleep(2)
            send_button  = self.driver.find_element(By.XPATH, "//button[starts-with(@aria-label,'Send without a note')]")
            send_button.click()
            time.sleep(5)


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
        time.sleep(5)
        # self.search_jobs()
        # time.sleep(10)
        # self.send_messages()
        self.apply_filters()
        self.close_session()

if __name__ == '__main__':

    with open('config.json') as config_file:
        data = json.load(config_file)
    
    bot = JobSearch(data)
    # bot.send_messages()
    '''
    This is not functional
    # bot.apply_filters()
    '''
    bot.send_connection()
    time.sleep(5)
    bot.close_session()

