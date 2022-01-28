import requests
from bs4 import BeautifulSoup


def prices_from_soup(prices, links):
    for link in links:
        row_price = link.find('span', attrs={'data-ftid':'bull_price'}).text
        price = int(row_price.replace('\xa0',''))       
        prices.append(price)
    return prices
        

def parser_prices(manufacturer, model, production_year):
    url_drom = f'https://auto.drom.ru/{manufacturer}/{model}/year-{production_year}/'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'),
    }
    r=requests.get(url_drom, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(r.text, 'html.parser')
    all_links = soup.find_all('a', class_="css-3jcp5o")
    prices = []
    prices = prices_from_soup(prices, all_links)
    all_pages = soup.find_all('a', class_="css-98q0l3 ena3a8q0")
    for page in range(2,(len(all_pages)+1)):
        url_drom = f'https://auto.drom.ru/{manufacturer}/{model}/year-{production_year}/page{page}/'
        r=requests.get(url_drom, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        all_links = soup.find_all('a', class_="css-3jcp5o")
        prices = prices_from_soup(prices, all_links)
    return(prices)