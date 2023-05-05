from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep 
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient('localhost', 27017)
db = client.scientific_articles
articles_to_scrape = db.articles_to_scrape

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


offset = 0

while offset<1000:
    driver.get("https://www.sciencedirect.com/search?qs=generative%20ai&date=2023&articleTypes=FLA&accessTypes=openaccess&sortBy=date&show=100&offset=" + str(offset))
    sleep(2)

    result_container = driver.find_element(by=By.XPATH, value='//ol[@class="search-result-wrapper"]')
    results = result_container.find_elements(by=By.XPATH, value='.//li[@class="ResultItem col-xs-24 push-m"]')


    for result in results:
        link = result.find_element(by=By.XPATH, value='.//a').get_attribute('href')
        try:
            articles_to_scrape.insert_one({"link": link, "scraped": False})
        except DuplicateKeyError as e:
            continue

    offset += 100

        