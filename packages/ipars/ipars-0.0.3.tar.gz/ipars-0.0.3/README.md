# Библиотека для парсинга

Установить библиотеку:
```bash
pip install ipars
```

## Пример кода
```python
from ipars import Pars
p = Pars('https://google.com', './index.html')
p.get_static_page()
```

## Коротко о методах
1. Функция **get_static_page** принимает url страницы и сохраняет html по указанному пути. 

2. Функция **get_dinamic_page** с помощью библиотеки Selenium получает динамически обновляемую страницу. Это помогает когда контент на странице подгружается динамически

3. Функция **returnBs4Object** возвращает объект beautifulsoup4

4. Функция **deleteFile** удаляет файл по пути pathToSaveFile. Пишется в конце кода после выполнения работы парсера

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.
