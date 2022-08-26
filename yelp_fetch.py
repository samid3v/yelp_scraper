from bs4 import BeautifulSoup
import grequests
import pandas as pd
import time
  
def get_urls():
    urls = []
    location = input('Enter Location \t')             #change where you wanna search
    for x in range(0,240,10):
        urls.append("https://www.yelp.com/search?find_desc=live+music&find_loc="+location+"&start="+str(x))
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
        mains = sp.find_all('div', class_ = 'businessName__09f24__EYSZE display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY')
        main_url = 'https://www.yelp.com'
        for main in mains:
            a_tag = main.find('a', class_ = 'css-1m051bw').get('href')
            a_tag_formated = main_url + str(a_tag)
            business_page.append(a_tag_formated)
            print('Added: ', a_tag_formated)
    return business_page 

urls = get_urls()
# print(urls)
resp = get_data(urls)
df = pd.DataFrame(parse(resp))
df.to_csv('page_links.csv', index=False, header=False)
links = input('do you want to get urls? y/n\t')
if links=='y':
    start = time.perf_counter()
    header ='<html><body>'
    footer = '</body></html>'

    def get_links():
        reqs = [grequests.get(link) for link in (open('page_links.csv').readlines())]
        time.sleep(0.23)
        resp = grequests.map(reqs, size = 5)
        return resp

    def parse_links(resp):
        Names = []
        Address = []
        Websites = []
        Phones = []
        print('starting to fetch data')
        print('=======================================================')
        for r in resp:
            soup = BeautifulSoup(r.text, 'lxml')
            time.sleep(0.22)
            # mainPage = soup.find('div', class_ = 'main-content-wrap main-content-wrap--full')
            

            try:
                name = soup.find('h1', class_ = 'css-dyjx0f').get_text()
                Names.append(name)
            except AttributeError:
                name = 'NUll'
                Names.append(name)

            try:
                address = soup.find('p', class_ = 'css-qyp8bo').get_text()
                Address.append(address)
            except AttributeError:
                address = 'Null'
                Address.append(address)
            except TypeError:
                address = 'Null'
                Address.append(address)

            try:
                website = soup.find('div', class_ = 'css-1vhakgw border--top__09f24__exYYb border-color--default__09f24__NPAKY').find_next('div', class_ = 'arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG border-color--default__09f24__NPAKY').find_next('a', class_ = 'css-1um3nx').get_text()
                if website[:3] == 'get':
                    Websites.append('no website') 
                else:
                    Websites.append(website) 
                    
                    
                    
            except AttributeError:
                website = 'Null'
                Websites.append(website)
            try:
                phone = soup.find_all('p', class_ = 'css-1p9ibgf')
                if len(phone)>=2:
                    new =phone[-2]
                    ptag = BeautifulSoup(f'{header}{new}{footer}', 'html.parser')
                    newtag=ptag.find('p').get_text()
                    if newtag[:4] == 'http':
                        Phones.append('no mobile number')
                    else:
                        Phones.append(newtag)
                else:
                    Phones.append('null')
            except AttributeError:
                phone = 'Null'
                Phones.append(phone)        
                
        print('Fetch completed successfully')
        print('Generating csv---------------------------------')
        dfs = pd.DataFrame({'live music Bars':Names, 'Address':Address, 'Website Links': Websites,'Phone Number': Phones})
        dfs.to_csv('Data.csv', index=False)
        cleandf= pd.read_csv('./Data.csv')
        cleandf.dropna(inplace=True)
        cleandf.to_csv('livemusic_Data.csv', index=False)

    res = get_links()
    parse_links(res)

    end = time.perf_counter()
    print('Time taken:', end-start)
