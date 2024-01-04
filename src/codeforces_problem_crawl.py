import json
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging

logging.basicConfig(filename='problem.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def random_sleep(start, end):
    time_sleep = random.uniform(start, end)
    time.sleep(time_sleep)

service = Service('chromedriver-linux64/chromedriver')

service.start()

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://codeforces.com/problemset')

problems = []

while True:
    logging.info(f'Crawl page {driver.current_url}')
    table = driver.find_elements(by=By.XPATH, value="//table[@class='problems']//tr")
    for row in table:
        problem_metadata = {}
        for idx, td in enumerate(row.find_elements(by=By.XPATH, value='.//td')):
            class_name = td.get_attribute("class")
            if idx == 0:
                problem_link = td.find_element(by=By.XPATH, value='.//a').get_attribute('href')
                problem_metadata['id'] = td.text
                problem_metadata['link'] = problem_link
            if idx == 1:
                problem_name = td.text.split('\n')[0]
                try:
                    problem_type = td.text.split('\n')[1]
                except Exception as e:
                    problem_type = ''
                problem_metadata['problem_name'] = problem_name
                problem_metadata['problem_type'] = problem_type
            if idx == 2:
                continue
            if idx == 3:
                problem_metadata['rating'] = td.text
            if idx == 4:
                submission = td.text.strip().replace('x', '')
                try:
                    submission_page_link = td.find_element(by=By.XPATH, value='.//a').get_attribute('href')
                except Exception as e:
                    submission_page_link = ""
                problem_metadata['submission'] = submission
                problem_metadata['submission_page_link'] = submission_page_link
            logging.info(f'{idx}, {class_name}, {td.text}')
        problems.append(problem_metadata)
        f = open('problems.json', 'w')
        json.dump(problems, f, indent=4)
    
    next_button = driver.find_element(by=By.XPATH, value="//a[contains(text(), '→')]")
    if next_button:
        next_button_href = next_button.get_attribute('href')
        driver.get(next_button_href)
        random_sleep(1, 5)
    else:
        break

driver.quit()

f = open('problems.json', 'w')
json.dump(problems, f, indent=4)