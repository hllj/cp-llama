import json
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup, Tag

import logging

logging.basicConfig(filename='problem_statement.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def process_math(soup):
    for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
        mathjax_span.replace_with('')

    for script in soup.find_all('script', {'type': 'math/tex'}):
        text = '$' + script.get_text() + '$'
        script.replace_with(text)
    
    return soup

def process_section_title(soup):
    for div in soup.find_all('div', {'class': 'section-title'}):
        div.replace_with('')
    
    return soup

def process_list(soup):
    for li in soup.find_all('li'):
        li.replace_with('\n - ' + li.get_text() + '\n')
    
    return soup

def extract_header(driver):
    # Extract Header
    try:
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
    except Exception as e:
        return ""
    

def extract_problem_statement(driver):
    try:
        # Extract Problem Statement

        problem_statement = driver.find_elements(by=By.XPATH, value="//div[@class='problem-statement']/div")[1]

        soup = BeautifulSoup(problem_statement.get_attribute('innerHTML'), 'html.parser')

        soup = process_math(soup)

        soup = process_section_title(soup)

        soup = process_list(soup)

        return soup.get_text()
    except Exception as e:
        return ""

def extract_input_format(driver):
    try:
        # Extract Input Format
        input = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='input-specification']")
        soup = BeautifulSoup(input.get_attribute('innerHTML'), 'html.parser')

        soup = process_math(soup)

        soup = process_section_title(soup)

        soup = process_list(soup)

        return soup.get_text()
    except Exception as e:
        return ""

def extract_output_format(driver):
    try:
        #Extract Output Format
        output = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='output-specification']")
        soup = BeautifulSoup(output.get_attribute('innerHTML'), 'html.parser')

        soup = process_math(soup)

        soup = process_section_title(soup)

        soup = process_list(soup)
        
        return soup.get_text()
    except Exception as e:
        return ""

def extract_sample_test(driver):
    try:
        #Extract Sample Test Cases
        sample_test = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='sample-tests']")
        soup = BeautifulSoup(sample_test.get_attribute('innerHTML'), 'html.parser')

        soup = process_math(soup)

        soup = process_section_title(soup)

        for div in soup.find_all('div', {'title': 'Copy'}):    
            div.replace_with('')    

        for div in soup.find_all('div', {'class': 'title'}):
            div.replace_with(div.get_text() + '\n')

        for div in soup.find_all('div', {'class': 'test-example-line'}):
            div.replace_with(div.get_text() + '\n')

        soup = process_list(soup)

        return soup.get_text()
    except Exception as e:      
        return ""

def extract_note(driver):
    try:
        #Extract Note
        note = driver.find_element(by=By.XPATH, value="//div[@class='problem-statement']/div[@class='note']")
        soup = BeautifulSoup(note.get_attribute('innerHTML'), 'html.parser')

        soup = process_math(soup)

        soup = process_section_title(soup)

        for div in soup.find_all('div', {'class': 'title'}):
            div.replace_with(div.get_text() + '\n')

        for div in soup.find_all('div', {'class': 'test-example-line'}):
            div.replace_with(div.get_text() + '\n')

        soup = process_list(soup)

        return soup.get_text()
    except Exception as e:
        return ""

def crawl_problem_by_id(service, options, url):
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    header_data = extract_header(driver)

    problem_statement = extract_problem_statement(driver)

    logging.info('Problem Statement:' + problem_statement)

    input_format = extract_input_format(driver)

    logging.info('Input:' + input_format)

    output_format = extract_output_format(driver)

    logging.info('Output:' + output_format)

    sample_test = extract_sample_test(driver)

    logging.info('Sample Test:' + sample_test)

    note = extract_note(driver)

    logging.info('Note:' + note)

    driver.quit()

    return header_data, problem_statement, input_format, output_format, sample_test, note

def random_sleep(start, end):
    time_sleep = random.uniform(start, end)
    time.sleep(time_sleep)

if __name__ == '__main__':
    service = Service('chromedriver-linux64/chromedriver')

    service.start()

    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    options.add_argument('incognito')
    options.add_argument('--headless')

    f = open('problems.json', 'r')
    problems = json.load(f)

    problem_statements = []

    for problem in problems:
        url = problem['link']
        logging.info(f'Crawl problem statement {url}')
        random_sleep(1, 5)
        header_data, problem_statement, input_format, output_format, sample_test, note = crawl_problem_by_id(service, options , url)
        problem_statements.append({
            'id': problem['id'],
            'link': url,
            'problem_name': problem['problem_name'],
            'problem_type': problem['problem_type'],
            'rating': problem['rating'],
            'submission': problem['submission'],
            'submission_page_link': problem['submission_page_link'],
            'header_data': header_data,
            'problem_statement': problem_statement,
            'input_format': input_format,
            'output_format': output_format,
            'sample_test': sample_test,
            'note': note
        })
        f = open('problem_statements.json', 'w')
        json.dump(problem_statements, f, indent=4)

    service.stop()
    f = open('problem_statements.json', 'w')
    json.dump(problem_statements, f, indent=4)
