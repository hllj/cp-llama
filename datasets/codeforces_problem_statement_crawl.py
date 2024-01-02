import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup, Tag

service = Service('chromedriver-linux64/chromedriver')

service.start()

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_argument('incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(service=service, options=options)

driver.get('https://codeforces.com/problemset/problem/1895/G')

# Extract Header

header = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='header']")

header_data = {}

for idx, div in enumerate(header.find_elements(by=By.XPATH, value="./div")):
    if div.get_attribute('class') == 'title':
        header_data['title'] = div.text
    
    if div.get_attribute('class') != 'title':
        key = div.find_element(by=By.XPATH, value="./div[@class='property-title']").text.strip()
        value = div.text.replace(key, '').strip()
        header_data[key] = value

print('Header: ', header_data)

# Extract Problem Statement

problem_statement = driver.find_elements(by=By.XPATH, value="//div[@class='problem-statement']/div")[1]

soup = BeautifulSoup(problem_statement.get_attribute('innerHTML'), 'html.parser')

for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
    mathjax_span.replace_with('')

for script in soup.find_all('script', {'type': 'math/tex'}):
    text = '$' + script.get_text() + '$'
    script.replace_with(text)

for div in soup.find_all('div', {'class': 'section-title'}):
    div.replace_with('')

for li in soup.find_all('li'):
    li.replace_with(li.get_text() + '\n')

print('Problem Statement:', soup.get_text())

# Extract Input Format
input = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='input-specification']")
soup = BeautifulSoup(input.get_attribute('innerHTML'), 'html.parser')

for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
    mathjax_span.replace_with('')

for script in soup.find_all('script', {'type': 'math/tex'}):
    text = '$' + script.get_text() + '$'
    script.replace_with(text)

for div in soup.find_all('div', {'class': 'section-title'}):
    div.replace_with('')

for li in soup.find_all('li'):
    li.replace_with(li.get_text() + '\n')

print('Input:', soup.get_text())

#Extract Output Format
output = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='output-specification']")
soup = BeautifulSoup(output.get_attribute('innerHTML'), 'html.parser')

for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
    mathjax_span.replace_with('')

for script in soup.find_all('script', {'type': 'math/tex'}):
    text = '$' + script.get_text() + '$'
    script.replace_with(text)

for div in soup.find_all('div', {'class': 'section-title'}):
    div.replace_with('')

for li in soup.find_all('li'):
    li.replace_with(li.get_text() + '\n')

print('Output:', soup.get_text())

#Extract Sample Test Cases
sample_test = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='sample-tests']")
soup = BeautifulSoup(sample_test.get_attribute('innerHTML'), 'html.parser')

for div in soup.find_all('div', {'title': 'Copy'}):    
    div.replace_with('')

for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
    mathjax_span.replace_with('')

for script in soup.find_all('script', {'type': 'math/tex'}):
    text = '$' + script.get_text() + '$'
    script.replace_with(text)

for div in soup.find_all('div', {'class': 'section-title'}):
    div.replace_with(div.get_text() + '\n')

for div in soup.find_all('div', {'class': 'title'}):
    div.replace_with(div.get_text() + '\n')

for div in soup.find_all('div', {'class': 'test-example-line'}):
    div.replace_with(div.get_text() + '\n')

for li in soup.find_all('li'):
    li.replace_with(li.get_text() + '\n')


print('Sample Test:', soup.get_text())

#Extract Note
note = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='note']")
soup = BeautifulSoup(note.get_attribute('innerHTML'), 'html.parser')

for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
    mathjax_span.replace_with('')

for script in soup.find_all('script', {'type': 'math/tex'}):
    text = '$' + script.get_text() + '$'
    script.replace_with(text)

for div in soup.find_all('div', {'class': 'section-title'}):
    div.replace_with(div.get_text() + '\n')

for div in soup.find_all('div', {'class': 'title'}):
    div.replace_with(div.get_text() + '\n')

for div in soup.find_all('div', {'class': 'test-example-line'}):
    div.replace_with(div.get_text() + '\n')

for li in soup.find_all('li'):
    li.replace_with(li.get_text() + '\n')


print('Note:', soup.get_text())