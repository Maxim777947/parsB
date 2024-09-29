from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import time
from transliterate import translit, slugify
import httplib2
from PIL import Image
import pytesseract




# browser = webdriver.Chrome()
# Начальная страница 
# page = '/catalog/bearings?H1=1&H4=9091&H3=15580'
# domean = 'https://handel.pro'
# parser_list_bearing(domean, page)
start = time.perf_counter()


def parser_bearing(domean, pag):
    """Получаем ссылки всех подшипников со страницы"""
    page = requests.get(domean + pag)
    soup = BeautifulSoup(page.text, "lxml")
    #########################################
    #  создаём словарь с содежимым типа (' 1580205   CRAFT', '/goods/CRAFT~1580205')
    categoriess=soup.find_all('a', {'class':['popup-img']})
    treeppp = {}
    for x in categoriess:
        treeppp[x.findNext('a').text]=x.findNext('a').get('href')
    return treeppp


def bearing_haracteristik(domen, page):
    """ещем ссылку на характеристики в конткретном подшипнике"""
    page = requests.get(domen + page)
    soup = BeautifulSoup(page.text, "lxml")
    categoriess=soup.find('a', string='Характеристики')
    return categoriess['href']


def download_image(page, name='1111', format='jpg'):
    """Скачивание изображения в текущий каталог"""
    h = httplib2.Http('.cache')
    response, content = h.request(page)
    out = open(name + '.' + format, 'wb')
    out.write(content)
    out.close()
    return name + '.' + format


def read_image(route):
    """Чтение текста с картинки"""
    image = Image.open(route)
    string = pytesseract.image_to_string(image, lang='rus',)
    return string


def haracteristik(domean, page):
    """Создали словарь с характеристиками"""
    page = requests.get(domean + page)
    soup = BeautifulSoup(page.text, "lxml")
    data = soup.find_all('dl', {'class':['product-spec']})
    data_list = {}
    manufacturer = soup.find('h2', {'class':['page-title margin-top-clear goods-manufacturer']})
    article = soup.find('h1', {'class':['goods-name']})
    data_list['manufacturer'] = manufacturer.text.strip("\n")
    data_list['article'] = article.text.strip("\n")
    for x in data:
        key = x.find('span', {'class':['product-spec__name-inner']}).text.strip("\n ")
        
        try:
            value = x.find('img')['src']
            # print(key, value)
            srting = read_image(download_image(value))
            data_list[key] = srting.strip("\n")
        except TypeError:
            value = x.find('span', {'class':['product-spec__value-inner']}).text.strip("\n ")
            data_list[key] = value
        
    #{'manufacturer': 'INA','article': ' AXW10  ', 'Тип подшипника': 'Подшипник', 'Тип тела качения': 'Игольчатый',}
    for i in data_list.items():
        print(i)





finish = time.perf_counter()
print('Время работы: ' + str(finish - start))

