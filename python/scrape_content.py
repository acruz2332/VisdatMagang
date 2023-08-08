from bs4 import BeautifulSoup
import requests
import mechanicalsoup
from urllib.request import urlopen
import requests
import mechanicalsoup
from pymongo import MongoClient

#connect to mongo localhost
conn = MongoClient('192.168.4.17', 27017)
db = conn.dbmagang

collection = db.links_collection

titles_old = []
for x in collection.find():
    titles_old.append(x.get('title'))

url = 'https://www.detik.com/terpopuler'
req = requests.get(url)
content= req.text

soup=BeautifulSoup(content)

raw=soup.findAll(attrs={'class':'list-content__item'})

titles = []
links = []

for html in raw:
    a = (html.find(attrs={'class':'media__text'})).find('a')
    if a.get_text() not in titles_old:
        titles.append(a.get_text())
        links.append(a.get('href'))
    else:
        continue

for i, j in zip(titles, links):
    collection.insert_one({"title": i, "link": j})

#get mechanicalsoup for open html link
browser = mechanicalsoup.Browser()

#get article id from websites
def get_article_id(url):
    page = browser.get(url)
    soup = page.soup
    articleid = soup.find(attrs={'name':'articleid'})
    return articleid["content"]

#get article title from website
def get_title_news(url):
    page = browser.get(url)
    soup = page.soup
    title = soup.find(attrs={'name':'originalTitle'})
    return title["content"]
#get resource content

resource_content = []

def get_content_from_browser(ctn, url):
    try:
        page = browser.get(url)
        soup = page.soup
        if (soup.find(attrs={'class':'itp_bodycontent_wrapper'})):
            content = soup.find(attrs={'class':'itp_bodycontent_wrapper'})
            ctn = ctn+content.get_text()
            if (soup.find(attrs={'class':'detail__multiple'})):
                if (soup.find(attrs={'class':'detail__multiple'}).find(attrs={'class':'btn--paging'})):
                    new_link = soup.find(attrs={'class':'detail__multiple'}).find(attrs={'class':'btn--paging'}).get('href')
                    get_content_from_browser(ctn, new_link)
                else:
                    resource_content.append(ctn)
            else:
                resource_content.append(ctn)
        else:
            resource_content.append(None)
    except:
        resource_content.append(None)

def get_label_news(url):
    page = browser.get(url)
    soup = page.soup
    if (soup.find(attrs={'class':'detail__label'})):
        label = soup.find(attrs={'class':'detail__label'})
        return label.get_text().replace("detik","")
    else:
        return None
    
def get_create_date(url):
    page = browser.get(url)
    soup = page.soup
    if (soup.find(attrs={'name':'createdate'})):
        createdate = soup.find(attrs={'name':'createdate'})
        return createdate["content"]
    else:
        return None
    
def get_publish_date(url):
    page = browser.get(url)
    soup = page.soup
    if (soup.find(attrs={'name':'publishdate'})):
        publishdate = soup.find(attrs={'name':'publishdate'})
        return publishdate["content"]
    else:
        return None
    
def get_keywords(url):
    page = browser.get(url)
    soup = page.soup
    keywords = soup.find(attrs={'name':'keywords'})
    return keywords["content"]

collection_detik = db.detik_data

first_index = len(list(collection_detik.find()))

counter = 0

for i in collection.find()[first_index:]:
    ids = get_article_id(i.get('link'))
    titles = get_title_news(i.get('link'))
    contents = get_content_from_browser("",i.get('link'))
    labels = get_label_news(i.get('link'))
    createdates = get_create_date(i.get('link'))
    publisheddates = get_publish_date(i.get('link'))
    keywords = get_keywords(i.get('link'))
    
    diction = {"id": ids, "title": titles, "content": resource_content[counter], "label": labels, "created date": createdates, "get published date": publisheddates, "keywords": keywords};
    collection_detik.insert_one(diction)
    counter += 1