import pyautogui
import requests
import time
from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = 'https://ebudget.mcfr.ua'

# Получение и запись в файл исходника страницы
def get_source_html(url):
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get(url)
        time.sleep(5)
        driver.find_element(By.TAG_NAME, 'body')
        with open("source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()

# Сбор и запись в файл ссылок страницы
def get_items_urls(file_path):
    with open(file_path) as file:
        src = file.read()

    soup = Bs(src, 'lxml')
    links = soup.find_all('a')

    urls = []
    for link in links:
        href = link.get('href')
        allowUrl = href.find('https')
        if href != '#' and allowUrl == -1:
            urls.append(URL + href)

    with open('urls.txt', 'w') as file:
        for url in urls:
            file.write(f"{url}\n")

    return "[INFO] Urls collect successful"


def get_urls(file_path):
    with open(file_path) as file:
        urls_list = [url.strip() for url in file.readlines()]
    urls_list.insert(0, URL)
    return urls_list


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

def main():
    # Получение ссылок на внутренние страницы
    # get_source_html(URL)
    # get_items_urls('C:\\Users\\38097\\PycharmProjects\\graber\\source.html')
    urls = get_urls('C:\\Users\\38097\\PycharmProjects\\graber\\urls.txt')
    for url in urls:
        download_page(url)

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


