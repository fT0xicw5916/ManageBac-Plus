from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException
import time
import logging


class ManagebacDriver:
    """
    Custom selenium driver class for fetching data from ManageBac.

    Credits to William Jin Huidong.
    """

    def __init__(self, username, password, microsoft=False):
        self.class_excludes = ["Homeroom", "Study Hall", "Bedtime", "SDL", "历史", "政治"]
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.logger = logging.getLogger("app.selen")

        self.classes_xpath = "/html/body/div[1]/div[1]/ul/li[4]/ul/*"
        self.grades_xpath = "/html/body/div/div[2]/aside/div/section[2]/div/*"
        self.tasks_xpath = "/html/body/div/div[2]/div[2]/div/section/div/div[3]/*"

        # Login procedure
        self.driver.get("https://huijia.managebac.cn/login")
        if microsoft:
            self.driver.find_element(By.ID, "microsoft").click()
            self.__send_keys_stale_element_by_id("i0116", username)
            self.__click_stale_element_by_id("idSIButton9")
            self.__send_keys_stale_element_by_id("i0118", password)
            self.__click_stale_element_by_id("idSIButton9")
            self.__click_stale_element_by_id("idBtn_Back")
            time.sleep(5)
        else:
            box_usr = self.driver.find_element(By.ID, "session_login")
            box_psw = self.driver.find_element(By.ID, "session_password")
            btn_log = self.driver.find_element(By.NAME, "commit")
            box_usr.send_keys(username)
            box_psw.send_keys(password)
            btn_log.click()
        self.logger.info(f"Login success (Username = '{username}', Password = '{password}', {"MS" if microsoft else "MB"})")

    def __send_keys_stale_element_by_id(self, id, v):
        while True:
            try:
                self.driver.find_element(By.ID, id).send_keys(v)
                break
            except (StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException):
                pass

    def __click_stale_element_by_id(self, id):
        while True:
            try:
                self.driver.find_element(By.ID, id).click()
                break
            except (StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException):
                pass

    def get_past_tasks(self, subject):
        # TODO
        self.driver.get("https://huijia.managebac.cn/student")

        unfiltered_li_classes = self.driver.find_elements(By.XPATH, self.classes_xpath)[:-1]
        name_and_url = None
        for unfiltered_li_class in unfiltered_li_classes:
            unfiltered_link = unfiltered_li_class.find_element(By.XPATH, 'a')
            unfiltered_text = unfiltered_link.find_element(By.XPATH, "span").get_attribute("innerHTML")

            if unfiltered_text == subject:
                name_and_url = (unfiltered_text, unfiltered_link.get_attribute("href"))
                break

        if name_and_url is None:
            self.logger.error(f"Subject not found when trying to get past tasks for {subject}")
            return None

        self.driver.get(name_and_url[1] + "/core_tasks")
        tasks_list_divs = self.driver.find_elements(By.XPATH, self.tasks_xpath)[2:]
        tasks_list_divs = tasks_list_divs[::-1]  # Old task on top, latest task bottom

        past_tasks = {}
        for div in tasks_list_divs:
            name = div.find_element(By.XPATH, "div[1]/div[2]/h4/a").get_attribute("innerHTML")
            score_s = None

            try:  # Score task
                score_s = div.find_element(By.XPATH, "div[2]/div/div/div").get_attribute("innerHTML")
            except:  # Not a score task (Score task and/or Completed)
                try:  # Score task w/ completed
                    score_s = div.find_element(By.XPATH, "div[2]/div[1]/div/div").get_attribute("innerHTML")
                except:  # Completed
                    past_tasks[name] = 1
                    continue

            if score_s == "N/A":  # N/A task
                continue
            elif score_s is None or score_s == "":  # Not assessed yet
                continue
            score_l = score_s.split(" / ")
            score = float(score_l[0]) / float(score_l[1][:-4])
            past_tasks[name] = score

        return past_tasks

    def get_task_num(self, subject, category):
        self.driver.get("https://huijia.managebac.cn/student")

        unfiltered_li_classes = self.driver.find_elements(By.XPATH, self.classes_xpath)[:-1]
        name_and_url = None
        for unfiltered_li_class in unfiltered_li_classes:
            unfiltered_link = unfiltered_li_class.find_element(By.XPATH, 'a')
            unfiltered_text = unfiltered_link.find_element(By.XPATH, "span").get_attribute("innerHTML")

            if unfiltered_text == subject:
                name_and_url = (unfiltered_text, unfiltered_link.get_attribute("href"))
                break

        if name_and_url is None:
            self.logger.error(f"Subject not found when trying to get task number for {subject}/{category}")
            return None

        self.driver.get(name_and_url[1] + "/core_tasks")
        tasks_list_divs = self.driver.find_elements(By.XPATH, self.tasks_xpath)[2:]

        task_num = 0
        for div in tasks_list_divs:
            tags = [i.get_attribute("innerHTML") for i in div.find_elements(By.XPATH, "div[1]/div[2]/div/div/*")[1:-1]]
            if category[:category.find(' ')] in tags:
                task_num += 1

        return task_num

    def get_grades(self, tries=10):
        self.driver.get("https://huijia.managebac.cn/student")

        name_and_urls = []
        unfiltered_li_classes = self.driver.find_elements(By.XPATH, self.classes_xpath)[:-1]
        for unfiltered_li_class in unfiltered_li_classes:
            unfiltered_link = unfiltered_li_class.find_element(By.XPATH, 'a')
            unfiltered_text = unfiltered_link.find_element(By.XPATH, "span").get_attribute("innerHTML")

            filtered_out = False
            for class_exclude in self.class_excludes:
                if class_exclude in unfiltered_text:
                    filtered_out = True

            if not filtered_out:
                name_and_urls.append((unfiltered_text, unfiltered_link.get_attribute("href")))

        info_classes = []
        for (name, url) in name_and_urls:
            info_dict = {"class_name": name}

            info_grades = []
            count = 0
            done = False
            while count < tries and not done:
                count += 1

                self.driver.get(url + "/units")
                div_grades = self.driver.find_elements(By.XPATH, self.grades_xpath)[1:]

                for i, div_grade in enumerate(div_grades):
                    if i == 0:
                        name_with_prop = div_grade.find_element(By.XPATH, "div[1]/strong").get_attribute("innerHTML")  # Overall
                    else:
                        name_with_prop = div_grade.find_element(By.XPATH, "div[1]/div").get_attribute("innerHTML")  # Not overall
                    text_grade = div_grade.find_element(By.XPATH, "div[2]").get_attribute("innerHTML")

                    prop = int(name_with_prop[name_with_prop.find('(')+1:name_with_prop.find('%')]) / 100 if i else None
                    grade = float(text_grade[text_grade.find('(')+1:text_grade.find('%')]) if text_grade != "\n-\n" else None

                    info_grades.append((name_with_prop, grade, prop))

                if len(info_grades) > 0:
                    done = True
                    break

            if not done:
                self.logger.warning(f"Failed to retrieve GPA data for {name} ({url}) after {tries} tries")
                return None

            info_dict["grades"] = info_grades
            info_classes.append(info_dict)
            self.logger.info(f"Grade hit: {info_dict}")

        return info_classes

    def terminate(self):
        self.driver.quit()


if __name__ == "__main__":
    pass
