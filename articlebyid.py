from json import dumps
from random import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from utilities import check_exists_by_xpath, is_text_date, preprocess_webpage
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep 
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('localhost', 27017)
db = client.scientific_articles
articles_to_scrape_collection = db.articles_to_scrape
articles_to_scrape = db.articles_to_scrape.find({"scraped": False})
articles = db.articles
list_cur = list(articles_to_scrape)

chrome_options = Options()

prefs = {'profile.default_content_setting_values': {'popups': 2, 'geolocation': 2,
                                                    'notifications': 2}}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
chrome_options.add_argument("--start-maximized")

# chrome_options.add_argument('--headless')
driver = webdriver.Chrome(
    ChromeDriverManager().install(), options=chrome_options)

for article_to_scrape in list_cur:
    driver.get(article_to_scrape['link'])
    
    articles_to_scrape_collection.update_one({"link": article_to_scrape['link']}, {'$set': {"scraped": True}})

    sleep(0.8)
    public_date = ""

    if(check_exists_by_xpath(driver,'.//div[@id="publication"]')):
        candidate_public_dates = driver.find_element(By.XPATH,'.//div[@id="publication"]').find_elements(By.XPATH,'.//div[@class="text-xs"]')
        
        for elem in candidate_public_dates:
            if(is_text_date(elem.text.lower())):
                public_date = elem.text
                print(public_date)
                break
             
             
    driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight/3);")
    sleep(random())
    
    preprocess_webpage(driver)
    sleep(0.1)
    preprocess_webpage(driver)
    sleep(0.1)
    preprocess_webpage(driver)
    
    if(check_exists_by_xpath(driver, './/div[@id="body"]')):
        body = driver.find_element(by=By.XPATH, value='.//div[@id="body"]').text
    else:
        continue
    title = driver.find_element(by=By.XPATH, value='.//h1[@id="screen-reader-main-title"]').text

    author_block = driver.find_element(by=By.XPATH, value='.//div[@class="author-group"]')
    authors_block_list = author_block.find_elements(by=By.XPATH, value='.//span[@class="react-xocs-alternative-link"]')
    
    authors = [author.text for author in authors_block_list]
    highlights = ""
    if(check_exists_by_xpath(driver, './/div[@class="abstract author-highlights"]')):
        highlights = driver.find_element(by=By.XPATH, value='.//div[@class="abstract author-highlights"]').text
    
    abstract = ""
    if(check_exists_by_xpath(driver, './/div[@class="abstract author"]')):
        abstract = driver.find_element(by=By.XPATH, value='.//div[@class="abstract author"]').text
    
    try:
        articles.insert_one({"link": article_to_scrape['link'], "title": title, "public_date": public_date, "authors": authors, "abstract": abstract, "highlights": highlights, "body": body})
        
    except DuplicateKeyError as e:
        print("document already present in DB")
        continue