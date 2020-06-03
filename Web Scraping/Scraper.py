import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

url = 'https://www.cryptocompare.com/coins/list/USD/1'

driver = webdriver.Chrome()
driver.get(url)
response = driver.execute_script("return document.documentElement.outerHTML")
driver.quit()
soup = BeautifulSoup(response, 'lxml')


values = []
names = []
symbols = []
rows = []
directVolumes = []
totalVolumes = []
marketCaps = []
ratings = []
changes = []

for c in soup.find_all('tr', {'class': "ng-scope"}):
    rows.append(c)

for row in rows:
    name = row.find(('span', {'class': "desktop-name ng-binding"})).get_text()
    name = name.split()
    if len(name) == 3:
        names.append(name[0] + " " + name[1])
    else:
        names.append(name[0])
    symbols.append(name[-1])

for row in rows:
    r1 = row.find_all(('div', {'class': "current-price-value"}))
    value = r1[1].get_text().strip()
    directVolume = r1[2].get_text().strip()
    directVolume = directVolume.replace(",", "")
    if directVolume!='-':
        if directVolume[-1]=='k':
            directVolume=float(directVolume[1:-1])*(10**3)
        elif directVolume[-1]=='M':
            directVolume=float(directVolume[1:-1])*(10**6)
        elif directVolume[-1]=='B':
            directVolume=float(directVolume[1:-1])*(10**9)
        else:
            directVolume = float(directVolume[1:])

    totalVolume = r1[3].get_text().strip()
    totalVolume = totalVolume.replace(",", "")
    if totalVolume != '-':
        if totalVolume[-1] == 'k':
            totalVolume = float(totalVolume[1:-1]) * (10 ** 3)
        elif totalVolume[-1] == 'M':
            totalVolume = float(totalVolume[1:-1]) * (10 ** 6)
        elif totalVolume[-1] == 'B':
            totalVolume = float(totalVolume[1:-1]) * (10 ** 9)
        else:
            totalVolume = float(totalVolume[1:])

    marketCap = r1[5].get_text().strip()
    if marketCap != '-':
        if marketCap[-1] == 'k':
            marketCap = float(marketCap[1:-1]) * (10 ** 3)
        elif marketCap[-1] == 'M':
            marketCap = float(marketCap[1:-1]) * (10 ** 6)
        elif marketCap[-1] == 'B':
            marketCap = float(marketCap[1:-1]) * (10 ** 9)
        else:
            marketCap = float(marketCap[1:])

    rating = r1[6].get_text().strip()

    change = float(r1[-1].get_text().strip()[:-1])

    value = value[2:]
    value = value.replace(",", "")

    values.append(float(value))
    directVolumes.append(directVolume)
    totalVolumes.append(totalVolume)
    marketCaps.append(marketCap)
    ratings.append(rating)
    changes.append(change)

numpy_data = np.array([names, symbols, values, directVolumes, totalVolumes, marketCaps, ratings, changes])

df = pd.DataFrame(data=numpy_data)
df = df.transpose()
df.columns=["Name","Symbol","Price","Direct Volume","Total Volume","Market Cap","Rating","Change last 24 hours"]
pd.set_option('display.max_columns', 30)
print(df)


plt.show()
# df.to_csv('output.csv', index=False)
