from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

file = open("links.txt","r")
link_list = [e.replace('\n','') for e in file.readlines()]

client = MongoClient('localhost', 27017)
db = client.scientific_articles
articles_to_scrape_collection = db.articles_to_scrape

for link in link_list:
  try:
    articles_to_scrape_collection.insert_one({"link": link, "scraped": False})
  except DuplicateKeyError as e:
      print("document already present in DB")
      continue
