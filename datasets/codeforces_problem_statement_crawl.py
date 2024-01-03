import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup, Tag

def extract_header(driver):
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
    return header_data

def extract_problem_statement(driver):
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

    return soup.get_text()

def extract_input_format(driver):
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

    return soup.get_text()

def extract_output_format(driver):
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
    
    return soup.get_text()

def extract_sample_test(driver):
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

    return soup.get_text()

def extract_note(driver):
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

    return soup.get_text()

def crawl_problem_by_id(service, options, url):
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    header_data = extract_header(driver)

    print('Header: ', header_data)

    problem_statement = extract_problem_statement(driver)

    print('Problem Statement:', problem_statement)

    input_format = extract_input_format(driver)

    print('Input:', input_format)

    output_format = extract_output_format(driver)

    print('Output:', output_format)

    sample_test = extract_sample_test(driver)

    print('Sample Test:', sample_test)

    note = extract_note(driver)

    print('Note:', note)

    driver.quit()

    return header_data, problem_statement, input_format, output_format, sample_test, note

if __name__ == '__main__':
    service = Service('chromedriver-linux64/chromedriver')

    service.start()

    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    options.add_argument('incognito')
    options.add_argument('--headless')

    url = 'https://codeforces.com/problemset/problem/1917/E'

    header_data, problem_statement, input_format, output_format, sample_test, note = crawl_problem_by_id(service, options , url)