from selenium.webdriver.chrome.options import Options
from requests import get, RequestException
from selenium import webdriver
from time import sleep
from os import remove
from bs4 import BeautifulSoup
import json

class Pars:
    '''Библиотека для работы с файлами во время парсинга'''


    def __init__(self, url, pathToSaveFile, writeMethod='w'):
        """Конструктор"""
        self.url = url
        self.pathToSaveFile = pathToSaveFile
        self.writeMethod = writeMethod


    def loadJson(self, pathToJsonFile:str):
        """Получаем данные из json файла"""
        with open(pathToJsonFile) as jsonFile:
            src = json.load(jsonFile)
        return src 


    def dumpJson(self, data:any, pathToJsonFile:str):
        """Записываем данные в json файл"""
        with open(pathToJsonFile, 'w') as jsonFile:
            json.dump(data, jsonFile, indent=4, ensure_ascii=0)


    def returnBs4Object(self, myEncoding:str='utf8', parser:str='lxml'):
        """Возвращаем объект beautifulsoup"""
        with open(self.pathToSaveFile, encoding=myEncoding) as file:
            src = file.read()
        soup = BeautifulSoup(src, parser)
        return soup


    def deleteFile(self):
        """Удаляем файл после работы с ним"""
        remove(self.pathToSaveFile)


    def get_static_page(self, headers:dict):
        '''Получаем статическую страницу'''
        try:
            # Отправляем запрос
            req = get(self.url, headers=headers)
            req.raise_for_status()  # Проверка на ошибки HTTP

            # Записываем данные
            if self.writeMethod == 'w':
                src = req.text
                with open(self.pathToSaveFile, self.writeMethod, encoding='utf-8') as file:
                    file.write(src)
            elif self.writeMethod == 'wb':
                src = req.content
                with open(self.pathToSaveFile, self.writeMethod) as file:
                    file.write(src)
            else:
                raise ValueError("Неподдерживаемый метод записи: {}".format(self.writeMethod))

        # Обрабатываем ошибки
        except RequestException as e:
            print(f"Ошибка при запросе: {e}")
        except IOError as e:
            print(f"Ошибка при записи в файл: {e}")
        except Exception as e:
            print('Ошибка:')
            print(e)


    def get_dinamic_page(self, closeWindow:bool=1):
        '''Получаем динамическую страницу'''

        # Устанавливаем опции для Chrome WebDriver
        options = Options()
        if closeWindow:
            options.add_argument('--headless')

        # открываем браузер
        with webdriver.Chrome(options=options) as driver:
            driver.get(self.url)
            # Прокручиваем страницу до самого низа
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Прокручиваем до низа страницы
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Ждем загрузки страницы
                sleep(2)
                # Вычисляем новую высоту страницы
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            # Получаем HTML-код страницы
            html_content = driver.page_source
            # Сохраняем HTML-код в файл
            with open(self.pathToSaveFile, "w", encoding="utf-8") as file:
                file.write(html_content)
