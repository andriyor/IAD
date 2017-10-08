# from statistics import mean

import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_weather(city, month, year):
    r = requests.get('https://{}.nuipogoda.ru/{}-{}'.format(city, month, year))
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("tbody", {"id": "forecast"})
    monthly = []
    for t in table:
        date = t.findAll("div", {"class": "date"})
        maxt = t.findAll("span", {"class": "max"})
        mint= t.findAll("span", {"class": "min"})
        for d, ma, mi in zip(date, maxt, mint):
            ma = ma.text.replace('°', '')
            ma = ma.replace('+', '')
            # mi = mi.text.replace('°', '')
            # print(round(mean([int(ma), int(mi)])))
            # print(type(int(ma)), ma)
            monthly.append(ma)
    return monthly


def save_year(city, year):    
    ru_months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    en_months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    df = pd.DataFrame()    
    for ru, en in zip(ru_months, en_months):
        monthly = scrape_weather(city, ru, year)
        df[en] = pd.Series(monthly)

    df.to_csv('{}-{}.csv'.format(city, year), index=False)


if __name__ == '__main__':
    city = ['kiev', 'kobelyaki', 'izmail', 'izyum', 'ivano-frankovsk', 
            'kamenec-podolskiy', 'luck', 'lubny', 'zaporozhe', 'kolomiya', 'zhitomir',
            'nezhin-ukraina', 'odessa', 'rovno', 'rahov', 'sumy', 'uman']
    year = 2016
    for c in city:
        save_year(c, year)
        print('{} downloaded'.format(c))
