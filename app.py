from bs4 import BeautifulSoup 
import requests 
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
#Fix
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import re 
import pandas as pd 
import schedule
from datetime import datetime
from selenium.webdriver.chrome.options import Options

total = int(input("Total Page 1-9 : "))
url = "https://ftimember.off.fti.or.th/_layouts/membersearch/result.aspx?ts=0&TextS="
email_lis = []
name_lis = []
link_lis = []

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)

soup = BeautifulSoup(driver.page_source,'html.parser')

lis = soup.find_all('tr',{'align':'left'})
for i in lis: 
    name = i.find('a').text 
    print('Name : ',name)
    name_lis.append(name)

    link = "https://ftimember.off.fti.or.th/_layouts/membersearch/"+i.find('a')['href']
    print('Link : ',link)
    link_lis.append(link)

    resx = requests.get(link)
    soupx = BeautifulSoup(resx.content,'html.parser')
    
    address = soupx.find('span',{'id':'addr_email'}).find('a')['href']
    print(address)
    email_lis.append(address)

pagenext = driver.find_elements(By.CSS_SELECTOR,'tr')[-1].find_elements(By.CSS_SELECTOR,'td')[1]

pagenext.click()

# round 2 - 9 
for page in range(total):

  # url = "https://ftimember.off.fti.or.th/_layouts/membersearch/result.aspx?ts=0&TextS="

  soup = BeautifulSoup(driver.page_source,'html.parser')

  lis = soup.find_all('tr',{'align':'left'})
  for i in lis: 
    #name
    name = i.find('a').text 
    print('Name : ',name)
    name_lis.append(name)

    # link
    link = "https://ftimember.off.fti.or.th/_layouts/membersearch/"+i.find('a')['href']
    print('Link : ',link)
    link_lis.append(link)

    resx = requests.get(link)
    soupx = BeautifulSoup(resx.content,'html.parser')
    
    #email
    address = soupx.find('span',{'id':'addr_email'}).find('a')['href']
    print(address)
    email_lis.append(address)

  pagenext2 = driver.find_elements(By.CSS_SELECTOR,'tr')[-1].find_elements(By.CSS_SELECTOR,'td')[1]
  pagenext2.click()

df = pd.DataFrame()
df['ชื่อบริษัท'] = name_lis 

df['Email'] = email_lis 

df['Link'] = link_lis 

df.to_excel("company_full9to10.xlsx")
print("Finish Scrape")