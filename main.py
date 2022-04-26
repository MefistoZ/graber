import pyautogui
import time
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.common.by import By


# 1. если пользователь зарегистрирован - видит другой контент
# 1. Передавать аргументы в скрипт

URL = 'https://ebudget.mcfr.ua'

# Получение и запись в файл исходника страницы
def get_source_html(url):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(5)
        with open("source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as _ex:
        print(_ex)
    # finally:
    #     driver.close()
    #     driver.quit()


# Сбор и запись в файл ссылок страницы
def get_items_urls(file_path):
    with open(file_path, encoding="utf8") as file:
        src = file.read()
    soup = Bs(src, 'lxml')
    links = soup.find_all('a')
    current_urls = get_urls('urls.txt')
    urls = []
    for link in links:
        href = link.get('href')
        if href and hrefCheck(href):
            allow = href in current_urls
            if not allow:
                if href != '#' and href != '/' and href not in urls:
                    urls.append(href)

    with open('urls.txt', 'a', encoding="utf-8") as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collect successful"


def get_urls(file_path):
    with open(file_path, encoding="utf-8") as file:
        urls_list = [url.strip() for url in file.readlines()]
    # urls_list.insert(0, URL)
    return urls_list


# Скачивание страницы
def download_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(4)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(30)
    driver.close()
    driver.quit()


def store_link():
    urls = get_urls('urls.txt')
    if urls:
        for url in urls:
            get_source_html(URL + url)
            get_items_urls('source.html')
            with open('parsed_urls.txt', 'a', encoding="utf-8") as file:
                file.write(f"{url}\n")
    else:
        return '[ERROR] Нет ссылок в файле urls.txt'


# Проверка валидности ссылок
def hrefCheck(href):
    notAllowLinks = ['https', 'http', 'articleprint', 'viewpdf', 'e-profkiosk', 'question', 'mailto', 'tel', 'toword']
    for link in notAllowLinks:
        if href.find(link) != -1:
            return False

    return True


def main(args):
    # Получение ссылок на внутренние страницы
    urls = get_urls('urls.txt')
    if urls:
        store_link()
    else:
        get_source_html(URL)
        get_items_urls('source.html')
        store_link()

    # get_source_html(URL)
    # get_items_urls('C:\\Users\\38097\\PycharmProjects\\graber\\source.html')

    # for url in urls:
    #     download_page(url)


if __name__ == '__main__':
    main()

# Рабочее скачивание одной страницы динамического сайта
# driver = webdriver.Chrome()
# driver.get("https://ebudget.mcfr.ua/")
# time.sleep(4)
#
# pyautogui.hotkey('ctrl', 's')
# time.sleep(2)
# pyautogui.press('enter')
# time.sleep(100)
