from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import pandas as pd
import time
from bs4 import BeautifulSoup



def google_search_bot(dataset):
    result_list = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)

    for restaurant_name in dataset['Restaurant Name']:
        try:
            driver.get('https://www.google.com')
            search_box = driver.find_element(By.NAME, 'q')
            search_box.send_keys(restaurant_name + ' abidjan')
            search_box.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            all_links = []
            for _ in range(3):
                driver.execute_script("window.scrollBy(0, 600);")
                time.sleep(2)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                links = soup.find_all('a', {'jsname': 'UWckNb'})
                other_links = soup.find_all('a', {'class': 'xFAlBc'})
                
                for link in links + other_links:
                    all_links.append(link['href'])
            
            jumia = any('food.jumia.ci' in link for link in all_links)
            glovo = any('glovoapp.com' in link for link in all_links)

            if jumia and glovo:
                result_list.append('JumiaFood - Glovo')
            elif jumia:
                result_list.append('JumiaFood')
            elif glovo:
                result_list.append('Glovo')
            else:
                result_list.append('')
        except:
            result_list.append('error')

    dataset['Delivery Search Result'] = result_list

    dataset.to_excel('final_version_of_task.xlsx',index=False)

if __name__ == '__main__':
    chromedriver_autoinstaller.install()
    
    dataset = pd.read_excel('Bolt_Abidjan_Restaurant_Lists.xlsx')

    run = google_search_bot(dataset)