import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

def link(driver, links, domen, page):
    url = (f'{domen}&page={str(page)}')
    driver.get(url)

    items = driver.find_elements(By.CLASS_NAME, "name-desc")
    for item in items:
        link = item.find_element(By.CLASS_NAME, "name").get_attribute('href')
        links.append(link)

        print(link)

def info(driver, links, total):
    for link in links:
        driver.get(link)

        x = []
        try:
            x.append({
                'title': driver.find_element(By.XPATH, "//div[@class='product-info__main']//h1").text,
                'price': driver.find_element(By.CLASS_NAME, "price").text.replace(' ₽', ''),
                'article': driver.find_element(By.XPATH, "//div[@class='product-info__article--id']").text.replace('Код товара: ', ''),
                'availability': driver.find_element(By.XPATH, "//div[@class='price-card__text']").text,
                'link': link
            })
        except:
            x.append({
                'title': driver.find_element(By.XPATH, "//div[@class='product-info__main']//h1").text,
                'price': driver.find_element(By.CLASS_NAME, "price").text.replace(' ₽', ''),
                'article': driver.find_element(By.XPATH, "//div[@class='product-info__article--id']").text.replace('Код товара: ', ''),
                'availability': 'в наличии',
                'link': link
            })

        print(x)
        total.extend(x)

def save(total):
    with open('parser.csv', 'w', newline='') as ex:
        writer = csv.writer(ex, delimiter=';')
        writer.writerow(['название', 'цена', 'код товара', 'наличие', 'ссылка'])
        for dict in total:
            writer.writerow([dict['title'], dict['price'], dict['article'], dict['availability'], dict['link']])

def parser():
    domen = input('введите ссылку на hobby games: ')
    pages = int(input('введите сколько страниц: '))
    driver = webdriver.Chrome()

    links = []
    for page in range(1, pages + 1):
        link(driver, links, domen, page)

    total = []
    info(driver, links, total)

    save(total)
    os.startfile('parser.csv')

    driver.close()

parser()