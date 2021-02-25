import requests
import datetime
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from config import EMAIL


jobs = []

def job(self,title,summary,location,company):
  self.title=title
  self.summary=summary
  self.location=location
  self.company=company


options = Options()
options.headless = False
driver = webdriver.Chrome(options=options, executable_path="/usr/local/bin/chromedriver")
driver.get("https://www.indeed.com")
user_agent = driver.execute_script("return navigator.userAgent;")
print(user_agent)
try:
    wait = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#text-input-where")))
    what = driver.find_element_by_id("text-input-what")
    where = driver.find_element_by_id("text-input-where")
    where.send_keys(Keys.COMMAND, "A")
    where.send_keys(Keys.DELETE)
    what.send_keys("test software engineer")
    where.send_keys("virginia")
    search = driver.find_element_by_css_selector("#whatWhereFormId > div.icl-WhatWhere-buttonWrapper > button")
    search.click()
    wait=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#filter-dateposted > button > span")))
    listings = driver.find_elements_by_xpath('//div[contains(@class,"jobsearch-SerpJobCard") and contains(@class,"unifiedRow") and contains(@class,"row") and contains(@class,"result") and contains(@class,"clickcard")]')
    page=0
  
      
    if (driver.find_elements_by_css_selector("#resultsCol > nav > div > ul > li:nth-child(6) > a")):
         next_page=driver.find_element_by_css_selector("#resultsCol > nav > div > ul > li:nth-child(6) > a")
         next_page.click()
         

    while (driver.find_elements_by_css_selector("#resultsCol > nav > div > ul > li:nth-child(7) > a") and page < 5):
      #ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
      
      #listings = driver.find_elements_by_xpath('//div[contains(@class,"jobsearch-SerpJobCard") and contains(@class,"unifiedRow") and contains(@class,"row") and contains(@class,"result") and contains(@class,"clickcard")]')
      driver.implicitly_wait(random.randint(0, 4))
      page = page + 1
      if (driver.find_elements_by_css_selector("#resultsCol > nav > div > ul > li:nth-child(7) > a")):
         wait=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[contains(@class,"jobsearch-SerpJobCard") and contains(@class,"unifiedRow") and contains(@class,"row") and contains(@class,"result") and contains(@class,"clickcard")]')))
         listings = driver.find_elements_by_xpath('//div[contains(@class,"jobsearch-SerpJobCard") and contains(@class,"unifiedRow") and contains(@class,"row") and contains(@class,"result") and contains(@class,"clickcard")]')
         #listings = WebDriverWait(driver,3,ignored_exceptions=ignored_exceptions)\
         #.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"jobsearch-SerpJobCard") and contains(@class,"unifiedRow") and contains(@class,"row") and contains(@class,"result") and contains(@class,"clickcard")]')))
         #print(listings[0].text)
         butt=driver.find_element_by_css_selector('#popover-x > button')
         if butt:
          butt.click()

         for listing in listings:
              jobSummary=listing.find_element_by_xpath('.//div[@class="summary"]/ul').text
              jobTitle=listing.find_element_by_xpath('.//h2[@class="title"]/a').text
              jobCompany=listing.find_element_by_xpath('.//div[@class="sjcl"]/div/span[@class="company"]').text
              jobRating=listing.find_elements_by_xpath('.//div[@class="sjcl"]/div/span[@class="ratingsDisplay"]/a')
              jobLink=listing.find_element_by_xpath('.//h2[@class="title"]/a').get_attribute('href')
              wait=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'.//div[@class="sjcl"]/div[contains(@class,"location") and contains(@class,"accessible-contrast-color-location")]')))
              #jobLocation=listing.find_elements_by_css_selector('div.sjcl > div.location.accessible-contrast-color-location')
              #jobLocation=listing.find_element_by_xpath('.//div[@class="sjcl"]/div[contains(@class,"location") and contains(@class,"accessible-contrast-color-location")]')
              jobLocation=listing.find_elements_by_xpath('.//div[@class="sjcl"]/span[contains(@class,"location") and contains(@class,"accessible-contrast-color-location")]')
              print(jobTitle)
              print(jobSummary)
              print(jobCompany)
              if jobRating:
                print(jobRating[0].text)
              else:
                    jobRating=0
              
              location=""
              #if jobLocation
              if jobLocation:
                 location=jobLocation[0].text
              print("---------------------")
              #resultsCol > nav > div > ul > li:nth-child(6)
         try:
             wait=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#resultsCol > nav > div > ul > li:nth-child(7) > a")))
             if wait:
                next_page=driver.find_element_by_css_selector("#resultsCol > nav > div > ul > li:nth-child(7) > a")
                next_page.click()
             break
         except ElementNotInteractableException:
             print("ELEMENT NOT INTERACTABLE")
    
        
finally: 
  driver.quit()
