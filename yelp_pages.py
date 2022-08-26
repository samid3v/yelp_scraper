from bs4 import BeautifulSoup
import grequests    #for async requests
import pandas as pd
import time

def get_urls():
    urls = []
    search_item = 'restaurants'           #you can change for your search
    location = 'san francisco'             #change where you wanna search
    for x in range(0,20,10):
        urls.append("https://www.yelp.com/search?find_desc=" +search_item + "&find_loc="+location+"&start="+str(x))
    return urls

def get_data(urls):
    reqs = [grequests.get(link) for link in urls]
    time.sleep(0.15)
    resp = grequests.map(reqs, size=4)
    
    return resp

def parse(resp):
    business_page = []
    for r in resp:
        sp = BeautifulSoup(r.text, 'lxml')
        print(sp)
        
    #     mains = sp.find_all('div', class_ = 'businessName__09f24__EYSZE display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY')
    #     main_url = 'https://www.yelp.com'
    #     for main in mains:
    #         a_tag = main.find('a', class_ = 'css-1kb4wkh').get('href')
    #         a_tag_formated = main_url + str(a_tag)
    #         business_page.append(a_tag_formated)
    #         print('Added: ', a_tag_formated)
    # return business_page


urls = get_urls()
resp = get_data(urls)
parse(resp)
# print(resp)

# df = pd.DataFrame(parse(resp))
# df.to_csv('page_links.csv', index=False, header=False)
