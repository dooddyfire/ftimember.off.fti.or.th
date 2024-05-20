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

url = "https://ftimember.off.fti.or.th/_layouts/membersearch/result.aspx?ts=0&TextS="
email_lis = []
name_lis = []
link_lis = []
phone_lis = []
loc_lis = []
product_lis = []
member_lis = []

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get(url)

input("กรุณาเปลี่ยนหน้าเป็นหน้าที่จะดึงแล้วพิมพ์ 1 กด enter : ")

soup = BeautifulSoup(driver.page_source,'html.parser')

lis = soup.find_all('tr',{'align':'left'})
for i in lis: 
    name = i.find('a').text 
    print('Name : ',name)
    name_lis.append(name)

    link = "https://ftimember.off.fti.or.th/_layouts/membersearch/"+i.find('a')['href']
    print('Link : ',link)
    link_lis.append(link)

    resx = driver.get(link)
    soupx = BeautifulSoup(driver.page_source,'html.parser')
    
    address = soupx.find('span',{'id':'addr_email'}).find('a')['href']
    print(address)
    email_lis.append(address)

    phone = soupx.find('span',{'id':'addr_telephone'}).text 
    print(phone)
    phone_lis.append(phone)

    loc = soupx.find('span',{'id':'comp_address'}).text 
    print(loc)
    loc_lis.append(loc)

    product = driver.find_elements(By.CSS_SELECTOR,'table[border="0"]')[0].text.replace("ผลิตภัณฑ์และบริการ :","").strip()
    print(product)
    product_lis.append(product)

    members = " ".join([ c.text for c in driver.find_elements(By.CSS_SELECTOR,'table')[4].find_elements(By.CSS_SELECTOR,'tr')[1].find_elements(By.CSS_SELECTOR,'td')])
    print(members)
    member_lis.append(members)


#-- page 2 
# for x in driver.find_elements(By.CSS_SELECTOR,'tr')[-1].find_elements(By.CSS_SELECTOR,'td'): 
#    try:
#      print(x.get_attribute('innerHTML'))
#      elem = x.find_element(By.XPATH,).get_attribute('src')
#      pagenext_lis.append(elem)
#    except: 
#      continue

driver.get(url)
pagenext_lis =[ g for g in driver.find_element(By.CSS_SELECTOR, "tr[style*='background-color:#284775']").find_elements(By.CSS_SELECTOR,'a')]
print(pagenext_lis)

time.sleep(5)
pagenext_lis[1].click()

time.sleep(5)
# round 2 - 9 

for page in range(2,4): #11

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

    resx = driver.get(link)
    soupx = BeautifulSoup(driver.page_source,'html.parser')
    
    #email
    address = soupx.find('span',{'id':'addr_email'}).find('a')['href']
    print(address)
    email_lis.append(address)

    phone = soupx.find('span',{'id':'addr_telephone'}).text 
    print(phone)
    phone_lis.append(phone)


    loc = soupx.find('span',{'id':'comp_address'}).text 
    print(loc)
    loc_lis.append(loc)

    product = driver.find_elements(By.CSS_SELECTOR,'table[border="0"]')[0].text.replace("ผลิตภัณฑ์และบริการ :","").strip()
    print(product)
    product_lis.append(product)

    members = " ".join([ c.text for c in driver.find_elements(By.CSS_SELECTOR,'table')[4].find_elements(By.CSS_SELECTOR,'tr')[1].find_elements(By.CSS_SELECTOR,'td')])
    print(members)
    member_lis.append(members)

# pagenext_lis[count].click()
  driver.get(url)
  time.sleep(5)
  pagenext_lis =[ g for g in driver.find_element(By.CSS_SELECTOR, "tr[style*='background-color:#284775']").find_elements(By.CSS_SELECTOR,'a')]
  print(pagenext_lis)
  
  pagenext_lis[page].click()
  time.sleep(5)
    # round 2 - 9 
  

df = pd.DataFrame()
df['ชื่อบริษัท'] = name_lis 
df['เบอร์โทร'] = phone_lis 
df['ที่อยู่'] = loc_lis 
df['ผลิตภัณฑ์และบริการ'] = product_lis 
df['สมาชิก'] = member_lis
df['Email'] = email_lis 
df['Link'] = link_lis 

df.to_excel("company_full1to2.xlsx")
print("Finish Scrape")