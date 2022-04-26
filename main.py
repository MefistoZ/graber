import pyautogui
import time
from sys import argv
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.common.by import By


# 1. если пользователь зарегистрирован - видит другой контент
# 1. Передавать аргументы в скрипт

# Ссылка на главную сайта
URL = argv[1]
# Постфикс для названия файлов
POSTFIX = argv[2]
# Тип запуска скрипта сбор ссылок\скачивание сайта по ссылкам
MODE = argv[3]

# Получение и запись в файл исходника страницы
def get_source_html(url):
    driver = webdriver.Chrome()

    try:
        driver.get(url)
        time.sleep(5)
        with open('source_' + POSTFIX + '.html', "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


# Сбор и запись в файл ссылок страницы
def get_items_urls(file_path):
    with open(file_path, encoding="utf8") as file:
        src = file.read()
    soup = Bs(src, 'lxml')
    links = soup.find_all('a')
    current_urls = get_urls('urls_' + POSTFIX + '.txt')
    urls = []
    for link in links:
        href = link.get('href')
        if href and hrefCheck(href):
            allow = href in current_urls
            if not allow:
                if href != '#' and href != '/' and href not in urls:
                    urls.append(href.lower())

    with open('urls_' + POSTFIX + '.txt', 'a', encoding="utf-8") as file:
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
    urls = get_urls('urls_' + POSTFIX + '.txt')
    if urls:
        for url in urls:
            get_source_html(URL + url)
            get_items_urls('source_' + POSTFIX + '.html')
            with open('parsed_urls_' + POSTFIX + '.txt', 'a', encoding="utf-8") as file:
                file.write(f"{url}\n")
    else:
        return '[ERROR] Нет ссылок в файле urls_' + POSTFIX + '.txt'


# Проверка валидности ссылок
def hrefCheck(href):
    notAllowLinks = ['https', 'http', 'articleprint', 'viewpdf', 'e-profkiosk', 'question', 'mailto', 'tel', 'toword']
    for link in notAllowLinks:
        if href.find(link) != -1:
            return False

    return True

# Инициализация файлов
def init_file():
    # Файл в котором содержатся уникальные ссылки по котором будет происходить скачивание сайта
    open('urls_' + POSTFIX + '.txt',  'a+', encoding="utf-8")

    # Файл в который записывается каждая проверенная ссылка (на случай ошибки скрипта мы знаем на какой ссылке остановился скрипт)
    open('parsed_urls_' + POSTFIX + '.txt',  'a+', encoding="utf-8")

    # Файл в который записывается исходный код страницы - из него происходить сбор ссылок
    open('source_' + POSTFIX + '.html',  'a+', encoding="utf-8")

def store_page():
    urls = get_urls('urls_' + POSTFIX + '.txt')
    urls.insert(0, '/')
    print(urls)
    if urls:
        for url in urls:
            driver = webdriver.Chrome()
            try:
                driver.get(URL + url)
                time.sleep(4)
                pyautogui.hotkey('ctrl', 's')
                time.sleep(2)
                pyautogui.press('enter')
                time.sleep(5)
                # Сохранение обработанных сылок
                with open('downloaded_page_' + POSTFIX + '.txt', 'a', encoding="utf-8") as page:
                    page.write(f"{url}\n")

                # Удаление обработанной ссылки из файла ссылок
                list = get_urls('urls_' + POSTFIX + '.txt')
                list.remove(url)
                with open('urls_' + POSTFIX + '.txt', 'w', encoding="utf-8") as links:
                    for link in list:
                        links.write(f"{link}\n")

            except Exception as _ex:
                print(_ex)
            finally:
                driver.close()
                driver.quit()


def main():
    if MODE == 'links':
        # Создание файлов
        init_file()

        # Получение ссылок на внутренние страницы
        urls = get_urls('urls_' + POSTFIX + '.txt')
        if urls:
            store_link()
        else:
            get_source_html(URL)
            get_items_urls('source_' + POSTFIX + '.html')
            store_link()
    elif MODE == 'store':
        store_page()


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
