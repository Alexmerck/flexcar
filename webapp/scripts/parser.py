from audioop import avg
import requests
from bs4 import BeautifulSoup
from statistics import mean
# encoding = 'utf-8'

def parser_prices(manufacturer, model, production_year):
    url_autoru = f'https://auto.ru/moskva/cars/bmw/2er/all/?year_from=2015&year_to=2018'
    url_avito = f'https://www.avito.ru/moskva/avtomobili/bmw/1-seriya/e81e82e87e88-20042007-ASgBAgICA0Tgtg3klyjitg2qmijqtg3UhCk?cd=1&radius=0'
    url_drom = f'https://auto.drom.ru/{manufacturer}/{model}/year-{production_year}/'
    print(url_drom)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'),
    }

    r=requests.get(url_drom, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_links = soup.find_all('a', class_="css-3jcp5o")
    prices = []
    for link in all_links:
        string_link = str(link)
        start_price=string_link.index('"bull_price">')
        end_price=string_link.rindex('<!--')
        price = string_link[start_price+13:end_price]
        int_price = int(price.replace('\xa0',''))
        prices.append(int_price)
    all_pages = soup.find_all('a', class_="css-98q0l3 ena3a8q0")
    for page in range(2,(len(all_pages)+1)):
        url_drom = f'https://auto.drom.ru/{manufacturer}/{model}/year-{production_year}/page{page}/'
        r=requests.get(url_drom, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')#.decode('utf-8','ignore')
        all_links = soup.find_all('a', class_="css-3jcp5o")
        for link in all_links:
            string_link = str(link)
            start_price=string_link.index('"bull_price">')
            end_price=string_link.rindex('<!--')
            price = string_link[start_price+13:end_price]
            int_price = int(price.replace('\xa0',''))        
            prices.append(int_price)
    print(prices)
    return(prices)