from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

import pandas as pd

class NeetCodeScraper:
    def __init__(self, data):
        """Init parameters"""
        self.url = data['URL']
        self.csv_path = data['path']
        self.driver = webdriver.Firefox(data['firefox_path'])
        self.problem_names = []
        self.leetcode_links = []
        self.difficulties = []
        self.youtube_links = []
        self.categories = []

    def scrape_static_page(self):
        """
        scrapes static page under tab Neetcode All 
        """
        
        self.driver.get(self.url)
        self.driver.find_element(By.LINK_TEXT, '🔮  NeetCode All').click()

        html = self.driver.page_source
        soup = BeautifulSoup(html)

        for link in soup.find_all('a',href = True, class_ = 'table-text text-color' ):
            self.problem_names.append(link.text.strip())

        for link in soup.find_all('a',href = True, class_ = 'table-text text-color' ):
            self.leetcode_links.append(link['href'].strip())

        for link in soup.find_all('td',class_='diff-col'):
            self.difficulties.append(link.text.strip())
        print('static page successfully scraped')
        self.driver.close()

    def scrape_dynamic_page(self):
        """
        scrapes dynamic pages under tab Neetcode All 
        """
        self.driver.get(self.url)
        self.driver.find_element(By.LINK_TEXT, '🔮  NeetCode All').click()

        counter = 0
        for i in range(19):
            first = '/html/body/app-root/app-pattern-table-list/div/div[2]/app-pattern-table[' + str(i+1) + ']/'

            category_xpath = first + 'app-accordion/div/button'

            category_button =  WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, category_xpath)))
            category_button.click()   

            for j in range(59):
                second = 'app-accordion/div/div/app-table/div/table/tbody/tr[' + str(j+1) + ']/td[5]/div/button/fa-icon'
                vid_solution_xpath = first + second

                try:
                    #click Video Solution
                    element = driver.find_element(By.XPATH, vid_solution_xpath)
                    driver.execute_script("arguments[0].click()", element)

                    #scrape category
                    for link in soup.find('p',class_='ng-tns-c41-' + str(i)):
                        self.categories.append(link.text.strip())

                except NoSuchElementException:
                    continue

                #Scrape youtube url
                youtube_xpath = '/html/body/app-root/app-pattern-table-list/div/div[2]/app-pattern-table[' + str(i+1) + ']/app-accordion/div/div/app-table/app-modal[2]/div/div[2]/header/h1/a'
                youtube_link=driver.find_element(By.XPATH, youtube_xpath)
                self.youtube_links.append(youtube_link.get_attribute("href"))

                counter +=1

                #click close button
                close_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-pattern-table-list/div/div[2]/app-pattern-table[' + str(i +1) + ']/app-accordion/div/div/app-table/app-modal[2]/div/div[2]/footer/button/b')))
                close_button.click()
        print("dynamic page successfully scraped")


    def write_2_csv(self):
        """
        Write scraped data as csv to csv_path
        """
        self.driver.quit()
        data = {"Category": self.categories,
        "Difficulty": self.difficulties, 
        "Problems": self.problem_names, 
        "Links": self.leetcode_links,
        "Solutions": self.youtube_links}

        df = pd.DataFrame(data)
        df.to_csv(self.csv_path)



