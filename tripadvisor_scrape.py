from seleniumwire import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller



def scrape_restaurants_links():

    chromedriver_autoinstaller.install()
    restaurants_list = list()
    for page in range(0,360,30):

        url = f"https://www.tripadvisor.com/Restaurants-g297513-oa{page}-Abidjan_Lagunes_Region.html"
        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument('--blink-settings=imagesEnabled=false')
        
        driver =webdriver.Chrome(options=chrome_options)

        driver.get(url)
        print("url: ",url)
        for item in range(1,31,1):
            print(item)
            try:
                first_res = driver.find_element(By.XPATH,value = f'//*[@id="lithium-root"]/main/div/div[4]/div/div/div/div[2]/div[6]/span[{item}]/div/div/div[2]/header/div/div[2]/div[1]/div/a').get_attribute('href')
                restaurants_list.append(first_res)
            except:
                first_res = driver.find_element(By.XPATH,value = f'//*[@id="lithium-root"]/main/div/div[4]/div/div/div/div[2]/div[5]/span[{item}]/div/div/div[2]/header/div/div[2]/div[1]/div/a').get_attribute('href')
                restaurants_list.append(first_res)
                                                    
        driver.close()
    return restaurants_list

def scrape_restaurants_informations(links):
    chromedriver_autoinstaller.install()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(links)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        website_link_element = soup.find_all(class_='YnKZo Ci Wc _S C AYHFM')[0]
        website_link_element = website_link_element['href']
    except:
        website_link_element = ''
    try:
        address_link_element = soup.find_all(class_ = 'AYHFM')[1].text
    except:
        address_link_element = ''
    try:
        phone_link_element = soup.find_all(class_ = 'BMQDV _F Gv wSSLS SwZTJ')[1].text
    except:
        phone_link_element = ''
    try:
        restaurant_name_element = soup.find(class_='HjBfq').get_text()
    except:
        restaurant_name_element = ''
    return [links, restaurant_name_element, address_link_element, phone_link_element, website_link_element]

if __name__ == '__main__':
    run = scrape_restaurants_links()

    link_list,name_list,address_list,phone_list,website_list =list(),list(),list(),list(),list()

    for item in run:
        print(item)
        try:
            link,name,address,phone,website = scrape_restaurants_informations(item)
            link_list.append(link)
            name_list.append(name)
            address_list.append(address)
            phone_list.append(phone)
            website_list.append(website)
        except:
            link_list.append('')
            name_list.append('')
            address_list.append('')
            phone_list.append('')
            website_list.append('')

    df = pd.DataFrame()
    df['TripAdvisor link'] = link_list
    df['Restaurant Name'] = name_list
    df['Restaurant Address'] = address_list
    df['Phone Number'] = phone_list
    df['Website'] = website_list

    df.to_excel('tripadvisor_restaurants.xlsx',index=False)
