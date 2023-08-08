from bs4 import BeautifulSoup
import requests
from requests.structures import CaseInsensitiveDict
import mechanicalsoup
from urllib.request import urlopen
from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.dbmagang

collection = db.links_collection_kompas

titles_old = []
for x in collection.find():
    titles_old.append(x.get('title'))

url = 'https://indeks.kompas.com/'
req = requests.get(url)
content= req.text

soup=BeautifulSoup(content)

raw=soup.findAll(attrs={'class':'article__list__title'})

titles = []
links = []

for html in raw:
    a = html.find('a')
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
    try:
        page = browser.get(url)
        soup = page.soup
        script = soup.find('script')
        return ((script.text).split("\"content_id\": \"")[1]).split("\",")[0]
    except:
        return None

#get article title from website
def get_title_news(url):
    page = browser.get(url)
    soup = page.soup
    title = soup.find('title')
    return title.get_text()

#query for all pages
def query(url):
#     url = "https://www.kompas.com/food/read/2023/07/03/160400075/ichiran-ramen-hadir-di-bsd-tangsel-hingga-pekan-depan?page=all"
    headers = CaseInsensitiveDict()
    headers["authority"] = "www.kompas.com"
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["cache-control"] = "max-age=0"
    headers["cookie"] = "_pbjs_userid_consent_data=3524755945110770; _gcl_au=1.1.752574321.1687917504; _jxx=44096af0-1557-11ee-b1d2-9776ce79fa90; _jx=44096af0-1557-11ee-b1d2-9776ce79fa90; _cb=zuVDiBTSzNOBoCznN; _jxtdid=d6ff23be-a27e-4aca-b196-ab1acdd31269; _jxx=44096af0-1557-11ee-b1d2-9776ce79fa90; _jx=44096af0-1557-11ee-b1d2-9776ce79fa90; AviviD_uuid=08198945-9b41-49bc-8a14-1384007dcb05; webuserid=5a353165-5aa1-f84b-855a-3ab6769db371; AviviD_refresh_uuid_status=2; badge_session=2; _popupkgplus_tes_desktop_2=1; _jxtoko=eyJESURfSlMiOiJjTktMTWtYcERIcnNUMG9HSGhwSnN1VU9oRVBuSUNldElrbk5vRUU3b29rPSJ9; _jxtoko=eyJESURfSlMiOiJjTktMTWtYcERIcnNUMG9HSGhwSnN1VU9oRVBuSUNldElrbk5vRUU3b29rPSJ9; _gid=GA1.2.1132685717.1688375900; _badge_temp_session=1; badge_first_click=1; AMP_TOKEN=^%^24NOT_FOUND; _cb_svref=null; g_state=^{^^i_l^^:0,^^i_t^^:1688453300223^}; fjw=aFIxRzFTTnNyZXpxUDh1Z05wSUVJTzBQcFFzSXo5WExWYlY1QnEzQXpwQVJwd2lyOEJBZiszMzMyUHVzT2Yzcm5zc0dFaGZ3QmRzejJhYVJTSHp5QnozRm1lUEczblBONnZnTzNZekkyeWRoR2JVQkNyUEdKdkRFRm1sdHB1bDVDcXExdVQyaE1CZlZxeDVWWjk1ZWdtYkYvM01PM1B6ZzIySjA1cHM5cVVvL1J6OExXQkJoMnVCRHJmdU1PbFZwVmMyWjZYbmdDbDg1Sms3OVVuU2RnY1J5RlNLMkVMNkJGWkZ5YzBMUFNFU3dmMmRBdUM1ZklaZ1Brc3Z3M2VGQ0Jib2hsaUVENnpHQXRuMmlLKzdtcGY3ck53eTl6bS9heGhwOEFwT2IyTzV0V2lPWlRSdkRFOU5HeXlMVWNaZFordXVEdG9xWHNRdW5XbG0xSkRsbzJvdzJjelRyTDVRMExMZ0pDeVNGbXdEK0lxdG9HTnVjOTFkd2dZVlRaK01sczlKWEw1dm4vem9uR3gvUXVOcUpXT2lRYmxQT0hqd0RtaDJqek81VnhGST0^%^3D; kmp_uid=WlZJeFVVRm5jV0ZEYmpSdU1HSnJNR3BCYW1GcVUwbEpjRTlVVGpWeWNHMHZWRzEyUkdGUVNEQjNhRzk1YjFBM05WSkxPSEJFVmpaUWRXUndhRlpDZHpRd01qRkNkVWgwZDNKTFZEVnFRVVJsUTAxMlVVRTlQUT09; kmp_lgn=kompas; kmps_usrid=b51f91eaf9e013f1a80fdd80196094a9; ukid=b51f91eaf9e013f1a80fdd80196094a9; kmp_nm=QWd1c3RpbnVzIEFjcnV6; lgn_w=kompasid; kmp_uid_value=WlZJeFVVRm5jV0ZEYmpSdU1HSnJNR3BCYW1GcVUwbEpjRTlVVGpWeWNHMHZWRzEyUkdGUVNEQjNhRzk1YjFBM05WSkxPSEJFVmpaUWRXUndhRlpDZHpRd01qRkNkVWgwZDNKTFZEVnFRVVJsUTAxMlVVRTlQUT09; kmps_usrid_value=b51f91eaf9e013f1a80fdd80196094a9; vignette_cookies=1; verification=1; participant_loyalty=404_b51f91eaf9e013f1a80fdd80196094a9; _jxrecsessionseg=17; XKMPSS=djFyOXNWRXhCRGFlZnlHcEdCWTI0SlBTTUwwdG5RTnBBT1k0VHM2NDdFbXg5bGpkR2xKUWdlQ2pQV2FyUkNJNQ==; usermail=e2fe1e7b694b53eab90b8702c83269fa6a06d4b993f83516f6b48e75825bf320; xkmpss_value=djFyOXNWRXhCRGFlZnlHcEdCWTI0SlBTTUwwdG5RTnBBT1k0VHM2NDdFbXg5bGpkR2xKUWdlQ2pQV2FyUkNJNQ==; __uid2_advertising_token=AgAAA1T0BFhNJ9bEE2QJ31/CI0KQkuzHhJ59SqYa51/UVv6YjWXMuLCxTEpC3s7c+cmACXhA2NJgSn5xbFuXtzkjheaB/JuT+9oI4BY6QcOe159iE+/iG8hfNwVTV6hbYMZJlfqs50gdjJ4nmW1r37mketmqWRdMMqYB/CjbLbLBLuW7WQ==; __uid2_advertising_token=AgAAA1T0BFhNJ9bEE2QJ31/CI0KQkuzHhJ59SqYa51/UVv6YjWXMuLCxTEpC3s7c+cmACXhA2NJgSn5xbFuXtzkjheaB/JuT+9oI4BY6QcOe159iE+/iG8hfNwVTV6hbYMZJlfqs50gdjJ4nmW1r37mketmqWRdMMqYB/CjbLbLBLuW7WQ==; _jxu2aux=^{^^rt^^:^^\"AAAAA1XUnepex3frSB4a+rwc7KB1bU1H6FjH5tcbDfqwrsjSEHE7XiORfZVA361KOegaNnUH20KCj5XrU+X3EoF7LGXtp7PgrAVZ5VBJjARlNOGmzgKmRxgM+UybtykCv75IR1lmvDTSYbNyctdCHin4eCrM1XNq14NU57vPGfuyijoSICYqQGitZn7BjncNkD+EH+GfWdgUOZdqKHHxDlqqVRhmY/r4iNbRa5NsAP/NmNyJRmT0sKmThMsiRC/cFqEhxh7heYYpdBE+fpQRUt4xyQnKUWmyOaVBC4ymP4S0gUSkD88QuuGXztwyW5TXZDZpxisLB2ZYUssikQ8W2JHHKu1cPGVxmhw4RUNi0e1bzBtKPGGXfL/wV52wQ45h4mm7^^\",^^\"te^^\":1688537508395,^^\"re^^\":1691043108395,^^\"rf^^\":1688454708395,^^\"rrk^^\":^^\"BxLwxdztprgveUqorAq7OdHtnKYa1Q3tnbZyLYcT6tE=^^\"^}; _jxu2aux=^{^^\"rt^^\":^^\"AAAAA1XUnepex3frSB4a+rwc7KB1bU1H6FjH5tcbDfqwrsjSEHE7XiORfZVA361KOegaNnUH20KCj5XrU+X3EoF7LGXtp7PgrAVZ5VBJjARlNOGmzgKmRxgM+UybtykCv75IR1lmvDTSYbNyctdCHin4eCrM1XNq14NU57vPGfuyijoSICYqQGitZn7BjncNkD+EH+GfWdgUOZdqKHHxDlqqVRhmY/r4iNbRa5NsAP/NmNyJRmT0sKmThMsiRC/cFqEhxh7heYYpdBE+fpQRUt4xyQnKUWmyOaVBC4ymP4S0gUSkD88QuuGXztwyW5TXZDZpxisLB2ZYUssikQ8W2JHHKu1cPGVxmhw4RUNi0e1bzBtKPGGXfL/wV52wQ45h4mm7^^\",^^\"te^^\":1688537508395,^^\"re^^\":1691043108395,^^\"rf^^\":1688454708395,^^\"rrk^^\":^^\"BxLwxdztprgveUqorAq7OdHtnKYa1Q3tnbZyLYcT6tE=^^\"^}; _cc_id=87d725eb2dc6d54b03d17b221fb652f7; panoramaId_expiry=1689055980981; panoramaId=231b59c875a848d4a494148ceb5216d5393845144af9e5a9380999ba07b99eca; panoramaIdType=panoIndiv; pbjs-unifiedid=^%^7B^%^22TDID^%^22^%^3A^%^22d6ff23be-a27e-4aca-b196-ab1acdd31269^%^22^%^2C^%^22TDID_LOOKUP^%^22^%^3A^%^22TRUE^%^22^%^2C^%^22TDID_CREATED_AT^%^22^%^3A^%^222023-06-04T06^%^3A13^%^3A01^%^22^%^7D; _au_1d=AU1D-0100-001688451182-LDKLLV9L-TAZ8; _au_last_seen_pixels=eyJhcG4iOjE2ODg0NTExODIsInR0ZCI6MTY4ODQ1MTE4MiwicHViIjoxNjg4NDUxMTgyLCJydWIiOjE2ODg0NTExODIsInRhcGFkIjoxNjg4NDUxMTgyLCJhZHgiOjE2ODg0NTExODIsImdvbyI6MTY4ODQ1MTE4Miwib3BlbngiOjE2ODg0NTExODIsInNtYXJ0IjoxNjg4NDUxMTgyfQ^%^3D^%^3D; _ga=GA1.1.504433896.1687917501; _gid=GA1.1.1132685717.1688375900; reaction:xml:2023:07:03:160400075=^{^^\"liked^^\":false,^^\"disliked^^\":false,^^\"saved^^\":false,^^\"total_liked^^\":0,^^\"kmps_usrid^^\":^^\"b51f91eaf9e013f1a80fdd80196094a9^^\"^}; __gads=ID=267fa6ee209fdc39:T=1687917503:RT=1688452258:S=ALNI_MbtTLxS69ObCb_zkFQlyNBNgLOMFg; __gpi=UID=00000c1aac7f4b3b:T=1687917503:RT=1688452258:S=ALNI_MYlQE0M7nng1UQsLqDR6ZNr_ttpDg; mp_a23050fa03288a8181f2681419e7815b_mixpanel=^%^7B^%^22distinct_id^%^22^%^3A^%^20^%^22^%^24device^%^3A188ffb91d65caf-0cd55c1d4ad399-26031d51-1fa400-188ffb91d65caf^%^22^%^2C^%^22^%^24device_id^%^22^%^3A^%^20^%^22188ffb91d65caf-0cd55c1d4ad399-26031d51-1fa400-188ffb91d65caf^%^22^%^2C^%^22^%^24initial_referrer^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^2C^%^22^%^24initial_referring_domain^%^22^%^3A^%^20^%^22^%^24direct^%^22^%^2C^%^22^%^24search_engine^%^22^%^3A^%^20^%^22google^%^22^%^7D; xkmpss_visitdate=2023-07-04T06:32:11.165Z; xkmpss_expiredate=2024-07-03T06:32:11.165Z; _jxxs=1688451000-44096af0-1557-11ee-b1d2-9776ce79fa90~1688452331; _jxxs=1688451000-44096af0-1557-11ee-b1d2-9776ce79fa90~1688452331; _jxs=1688451000-44096af0-1557-11ee-b1d2-9776ce79fa90~1688452331; _jxs=1688451000-44096af0-1557-11ee-b1d2-9776ce79fa90~1688452331; cto_bundle=AGdm4l9kQnZKd3VpQiUyQnRFRnB5aWJLQXZoNmxLcThsaFA1bFhiNlhzVkg0cGJzcERuZXp3U3g2Vk5kbGkxbTRqWTElMkJzTERpTVFxdnolMkJodWclMkJiYSUyRlpuJTJGalZwVm9MRWFwNlV3b0dHVDFVNU1hV1NqYWxPOExoWkxmeFVRRzN5MEdWMlU1UEtTU00xQzVBT2t6Und0ZE5wUkxERHclM0QlM0Q; _chartbeat2=.1687917528905.1688452331631.1001011.DnYoq0C1BAruCx6ERXgLA5FCliyf1.18; _ga_7KGEC8EBBM=GS1.1.1688445675.5.1.1688452331.59.0.0; _ga_77DJNQ0227=GS1.1.1688445675.5.1.1688452331.59.0.0; _ga_L32HM9P84T=GS1.2.1688445680.5.1.1688452331.60.0.0; MgidStorage=^%^7B^%^220^%^22^%^3A^%^7B^%^22svspr^%^22^%^3A^%^22^%^22^%^2C^%^22svsds^%^22^%^3A49^%^7D^%^2C^%^22C1341488^%^22^%^3A^%^7B^%^22page^%^22^%^3A2^%^2C^%^22time^%^22^%^3A^%^221688452332767^%^22^%^7D^%^2C^%^22C1410128^%^22^%^3A^%^7B^%^22page^%^22^%^3A1^%^2C^%^22time^%^22^%^3A^%^221688452333583^%^22^%^7D^%^2C^%^22C1410129^%^22^%^3A^%^7B^%^22page^%^22^%^3A2^%^2C^%^22time^%^22^%^3A^%^221688452333639^%^22^%^7D^%^2C^%^22C1439962^%^22^%^3A^%^7B^%^22page^%^22^%^3A3^%^2C^%^22time^%^22^%^3A^%^221688452333674^%^22^%^7D^%^2C^%^22C1439965^%^22^%^3A^%^7B^%^22page^%^22^%^3A1^%^2C^%^22time^%^22^%^3A^%^221688452263713^%^22^%^7D^%^2C^%^22C1439960^%^22^%^3A^%^7B^%^22page^%^22^%^3A2^%^2C^%^22time^%^22^%^3A^%^221688452333528^%^22^%^7D^%^2C^%^22C1439963^%^22^%^3A^%^7B^%^22page^%^22^%^3A1^%^2C^%^22time^%^22^%^3A^%^221688452333568^%^22^%^7D^%^2C^%^22C1439964^%^22^%^3A^%^7B^%^22page^%^22^%^3A1^%^2C^%^22time^%^22^%^3A^%^221688452263335^%^22^%^7D^%^7D; _ga=GA1.2.504433896.1687917501"
    headers["referer"] = "https://www.kompas.com/food/read/2023/07/03/160400075/ichiran-ramen-hadir-di-bsd-tangsel-hingga-pekan-depan?page=all"
    headers["sec-ch-ua"] = "^^\"Not.A/Brand^^\";v=^^\"8^^\", ^^\"Chromium^^\";v=^^\"114^^\", ^^\"Google Chrome^^\";v=^^\"114^^\""
    headers["sec-ch-ua-mobile"] = "?0"
    headers["sec-ch-ua-platform"] = "^^\"Windows^^\""
    headers["sec-fetch-dest"] = "document"
    headers["sec-fetch-mode"] = "navigate"
    headers["sec-fetch-site"] = "same-origin"
    headers["sec-fetch-user"] = "?1"
    headers["upgrade-insecure-requests"] = "1"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    
    resp = requests.get(url, headers=headers)
    return resp.content


#get resource content

def get_content_from_browser(url):
    page = browser.get(url)
    soup = page.soup
    try:
        if (soup.find(attrs={'class':'paging__link--show'})):
            newlink = url+'?page=all'
            content = query(newlink)
            soup2 = BeautifulSoup(content, 'html.parser')
            article_content = soup2.find(attrs={'class':'read__content'})
            if (article_content):
                return article_content.get_text()
            else:
                return None
        else:
            content = soup.find(attrs={'class':'read__content'})
            if (content):
                return content.get_text()
            else:
                return None
    except:
        return None
    
def get_label_news(url):
    page = browser.get(url)
    soup = page.soup
    if (soup.find(attrs={'name':'content_category'})):
        label = soup.find(attrs={'name':'content_category'})
        return label["content"]
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
    if (soup.find(attrs={'name':'content_PublishedDate'})):
        publishdate = soup.find(attrs={'name':'content_PublishedDate'})
        return publishdate["content"]
    else:
        return None
    
def get_keywords(url):
    page = browser.get(url)
    soup = page.soup
    keywords = soup.find(attrs={'name':'keywords'})
    return keywords["content"]

collection_kompas = db.kompas_data

first_index = len(list(collection_kompas.find()))

for i in collection.find()[first_index:]:
    try:
        ids = get_article_id(i.get('link'))
        titles = get_title_news(i.get('link'))
        contents = get_content_from_browser(i.get('link'))
        labels = get_label_news(i.get('link'))
        createdates = get_create_date(i.get('link'))
        publisheddates = get_publish_date(i.get('link'))
        keywords = get_keywords(i.get('link'))
    except:
        diction = {"id": ids, "title": titles, "content": contents, "label": labels, "created date": createdates, "get published date": publisheddates, "keywords": keywords};
        collection_kompas.insert_one(diction)
    