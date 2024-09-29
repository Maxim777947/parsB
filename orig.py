from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import time
from transliterate import translit, slugify
# from bearing.models import Bearing, RollingElementType, LoadDirection, TypeBearing


browser = webdriver.Chrome()
# Начальная страница 
page = '/goods/INA~AXW12'
domean = 'https://handel.pro'
# parser_list_bearing(domean, page)

start = time.perf_counter()


def parser_bearing(domean, pag):
    page = requests.get(domean + pag)
    """перебираем все подшиппнки со страницы page и заносим их в БД"""
    soup = BeautifulSoup(page.text, "lxml")
    #########################################
    #  создаём словарь с содежимым типа (' 1580205   CRAFT', '/goods/CRAFT~1580205')
    categoriess=soup.find_all('a', {'class':['popup-img']})
    treeppp = {}
    for x in categoriess:
        treeppp[x.findNext('a').text]=x.findNext('a').get('href')
    #########################################
    # перебераем страницу каждого подшипника из одной категории
    for cat, link in treeppp.items():
        # browser.maximize_window()
        browser.get('https://handel.pro'+link)
        cookies_1= {'domain': '.handel.pro', 'expiry': 1962580137, 'httpOnly': False, 'name': '_i****_session_cross_domain', 'path': '/', 'secure': False, 'value': 'WWJFaU8wMTBMSE9uVlR2YnRLKzlvdHE3MVgyTjVlS1JKVm1qMjVNK2JSbEYxcVZNQk9OR3A4VU1LUzZwY1lCeVlTNDVsSkFmUFNSRWt3cXdUYytxQlhnYk5BbnVoZktTMUJLRWQyaWxFeXRsR1ZCVzVnSGJRU0tLVVR0MjRYR2hXbXpaZnRnYWRzV0VnbmpjdjA5T1RzZEFkallmMEVySVA3ZkV3cjU5dVVaZjBmajU5bDIxVkEwbUQvSUVyWGdqaTc5WEJyT2tvNTVsWWx1TEZhQXB1L3dKUXl5aWpOQllEV245VStIajFDdXphWFQxVGVpeGJDV3JseU9lbE1vQmxhRklLa3BsRm9XUkNTakIrWXlDc3I5ZjdZOGgwYmplMFpGRGRxKzg3QTJFSGpkNWh5RmdxZzhpTXVvTUV5SFZnM2dzNHVqWkJRaTlwdmhkclEyNVNDSHJsVkZzeVpBaGc1ZmQ0NlhlSG43YnVHRUVDL0ZmUHVIelNhRkRZSVFYLS05UkJqM24yM0d4bjFBRWFVQjlYSzJnPT0%3D--e17089851778bedd374f240c353f399027fe0fb1'}
        cookies_2= {'domain': '.handel.pro', 'expiry': 1962580137, 'httpOnly': False, 'name': 'sa_current_city_coordinates_cross_domain', 'path': '/', 'secure': False, 'value': '%5B59.91815364%2C30.305578%5D'}
        cookies_3= {'domain': '.handel.pro', 'expiry': 1962580137, 'httpOnly': False, 'name': 'sa_current_city_cross_domain', 'path': '/', 'secure': False, 'value': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3'}
        browser.add_cookie(cookies_1)
        browser.add_cookie(cookies_2)
        browser.add_cookie(cookies_3)
        browser.get('https://handel.pro'+link)

        # url = 'https://handel.pro/goods/1GPZ~20884724?'
        urlo = 'https://handel.pro'
        page = requests.get(urlo + link)
        soup = BeautifulSoup(page.text, "lxml")

        # ищем ссылку на характеристики
        categoriess=soup.find('a', string='Характеристики')
        data_bearing_http = urlo + categoriess['href']

        #переходим по ссылке в характеристики
        page1 = requests.get(data_bearing_http)
        soup1 = BeautifulSoup(page1.text, "lxml")

        # выбираем html код содержащий характеристики
        data = soup1.find_all('dl', {'class':['product-spec']})

        # выбираем html код артикул и производителя
        data_list = {}
        manufacturer = soup1.find('h2', {'class':['page-title margin-top-clear goods-manufacturer']})
        article = soup1.find('h1', {'class':['goods-name']})
        data_list['manufacturer'] = manufacturer.text.strip("\n")
        data_list['article'] = article.text.strip("\n")

        # создали словарь c характеристиками по типу ('Тип подшипника', 'Подшипник ')
        for x in data:
            key = x.find('span', {'class':['product-spec__name-inner']}).text.strip("\n ")
            value = x.find('span', {'class':['product-spec__value-inner']}).text.strip("\n ")
            data_list[key] = value

        # for i in data:
        #     print(i)
        # for i in data_list.items():
        #     print(i)
        data_list
        s = Bearing(
            manufacturer=data_list['manufacturer'],
            article=data_list['article'],
            type_bearing=TypeBearing.objects.get(name=data_list['Тип подшипника']),
            element_type=RollingElementType.objects.get(name=data_list['Тип тела качения']),
            load_direction=LoadDirection.objects.get(name=data_list['Направление нагрузки']),
            number_rolling_tracks=data_list['Количество дорожек качения'],
            slug=slugify(data_list['manufacturer'] + 'производитель' + " " + data_list['article']),
            sealing=0,
        )
        s.save()


def parser_list_bearing(domean, pag):
    """ Возвращаем следующую страницу по номеру если она сущесвтует"""
    page = requests.get(domean + pag)
    soup = BeautifulSoup(page.text, "lxml")
    #########################################
    # словарь с содежимым типа (14, '/catalog/bearings/?H1=1&H4=2&H3=3&H2=4532&&page=14')
    categoriess=soup.find_all('li', {'class':['footable-page']})
    treeppp = {}
    for x in categoriess:
        try:
            treeppp[int(x.findNext('a').text)]=x.findNext('a').get('href')
        except ValueError:
            pass
    try:
        return treeppp[int(soup.find('li', {'class':['footable-page active']}).text) + 1]
    except KeyError:
        return None





#заходим в каждый каталог по очереди
# for link in lists:
while page is not None:
    browser.maximize_window()
    browser.get('https://handel.pro'+page)
    # cookies_1= {'domain': '.handel.pro', 'expiry': 1962580137, 'httpOnly': False, 'name': '_i****_session_cross_domain', 'path': '/', 'secure': False, 'value': 'WWJFaU8wMTBMSE9uVlR2YnRLKzlvdHE3MVgyTjVlS1JKVm1qMjVNK2JSbEYxcVZNQk9OR3A4VU1LUzZwY1lCeVlTNDVsSkFmUFNSRWt3cXdUYytxQlhnYk5BbnVoZktTMUJLRWQyaWxFeXRsR1ZCVzVnSGJRU0tLVVR0MjRYR2hXbXpaZnRnYWRzV0VnbmpjdjA5T1RzZEFkallmMEVySVA3ZkV3cjU5dVVaZjBmajU5bDIxVkEwbUQvSUVyWGdqaTc5WEJyT2tvNTVsWWx1TEZhQXB1L3dKUXl5aWpOQllEV245VStIajFDdXphWFQxVGVpeGJDV3JseU9lbE1vQmxhRklLa3BsRm9XUkNTakIrWXlDc3I5ZjdZOGgwYmplMFpGRGRxKzg3QTJFSGpkNWh5RmdxZzhpTXVvTUV5SFZnM2dzNHVqWkJRaTlwdmhkclEyNVNDSHJsVkZzeVpBaGc1ZmQ0NlhlSG43YnVHRUVDL0ZmUHVIelNhRkRZSVFYLS05UkJqM24yM0d4bjFBRWFVQjlYSzJnPT0%3D--e17089851778bedd374f240c353f399027fe0fb1'}
    # cookies_2= {'domain': '.handel.pro', 'expiry': 1962580137, 'httpOnly': False, 'name': 'sa_current_city_coordinates_cross_domain', 'path': '/', 'secure': False, 'value': '%5B59.91815364%2C30.305578%5D'}
    # cookies_3= {'domain': '.handel.pro', 'expiry': 1962580137, 'httpOnly': False, 'name': 'sa_current_city_cross_domain', 'path': '/', 'secure': False, 'value': '%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3'}
    # browser.add_cookie(cookies_1)
    # browser.add_cookie(cookies_2)
    # browser.add_cookie(cookies_3)
    # browser.get('https://handel.pro'+page)
    parser_bearing(domean, page)
    page = parser_list_bearing(domean, page)




finish = time.perf_counter()
print('Время работы: ' + str(finish - start))

