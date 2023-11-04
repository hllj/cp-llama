import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup, Tag

service = Service('/opt/homebrew/bin/chromedriver')

service.start()

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://codeforces.com/problemset/problem/1895/G')

# problem_statement = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']")

statement_divs = driver.find_elements(by=By.XPATH, value="//div[@class='problem-statement']/div")
problem_statement = {}

statement_paragraph = ""

for idx, section in enumerate(statement_divs):
    if idx == 0:
        continue
        # extract header
        for div in section.find_elements(by=By.XPATH, value='//div'):
            class_name = div.get_attribute('class')
            text = div.get_attribute('innerText')
            print(class_name, text)
            problem_statement[class_name] = text
    else:
        soup = BeautifulSoup(section.get_attribute('innerHTML'), 'html.parser')
        for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
            mathjax_span.replace_with('')
        for script in soup.find_all('script', {'type': 'math/tex'}):
            text = script.get_text()
            script.replace_with(text)
        for copy_div in soup.find_all('div', {'title': "Copy"}):
            copy_div.replace_with('')
        
        for p in soup.find_all(['p', 'div', 'pre']):
            if p.name != 'pre':
                statement_paragraph += p.get_text() + "\n"
            else:
                for div in p.find_all('div'):
                    statement_paragraph += div.get_text() + "\n"

print('final', statement_paragraph)