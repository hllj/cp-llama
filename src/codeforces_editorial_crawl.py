from html import unescape
import json
import os
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup, Tag

import logging

logging.basicConfig(filename='problem_editorial.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def process_math(soup):
    for mathjax_span in soup.find_all('span', {'class' : ['MathJax_Preview', 'MathJax']}):
        mathjax_span.replace_with('')

    for script in soup.find_all('script', {'type': 'math/tex'}):
        text = '$' + script.get_text() + '$'
        script.replace_with(text)
    
    return soup

def process_link(soup):
    for a in soup.find_all('a'):
        href = a.get('href')
        if 'problem' in href and 'contest' in href:
            title = a.get('title')
            a.replace_with(title)
    
    return soup

def crawl_tutorial(driver, url, contest_id, problem_id, problem_name):
    driver.get(url)
    random_sleep(1, 3)
    problem_name = contest_id + problem_id + ' - ' + problem_name

    print('check problem name', problem_name)

    curr_problem_name_id = contest_id + problem_id
    next_problem_name_id = contest_id + chr(ord(problem_id) + 1)
    content = driver.find_element(by=By.XPATH, value='//div[@class="content"]')
    soup = BeautifulSoup(content.get_attribute('innerHTML'), 'html.parser')

    soup = process_math(soup)

    soup = process_link(soup)

    text = soup.get_text()
    print('text', text)

    curr_index_string = text.find(curr_problem_name_id)

    next_index_string = text.find(next_problem_name_id)
    if next_index_string == -1:
        next_index_string = len(text)

    tutorial = text[curr_index_string:next_index_string]
    tutorial = tutorial.replace(problem_name, '')
    return tutorial

def random_sleep(start, end):
    time_sleep = random.uniform(start, end)
    time.sleep(time_sleep)

if __name__ == '__main__':
    service = Service('chromedriver-linux64/chromedriver')

    service.start()

    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
    options.add_argument('incognito')
    # options.add_argument('--headless')

    url = 'https://codeforces.com/problemset/problem/610/B'

    contest_id = url.split('/')[-2]
    problem_id = url.split('/')[-1]
    problem_name = "Vika and Squares"

    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)

    random_sleep(1, 3)

    material = driver.find_element(by=By.XPATH, value='//div[@class="roundbox sidebox sidebar-menu borderTopRound "]')

    urls = material.find_elements(by=By.XPATH, value='.//a')

    for url in urls:
        text = url.text.strip()
        print(url.get_attribute('href'), text)
        if text.find('Tutorial') != -1:
            tutorial = crawl_tutorial(driver, url.get_attribute('href'), contest_id, problem_id, problem_name)
            print('result', tutorial)
            break

    driver.quit()