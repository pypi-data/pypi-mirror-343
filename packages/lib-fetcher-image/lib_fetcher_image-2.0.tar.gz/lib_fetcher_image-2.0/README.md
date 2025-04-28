# lib-fetcher-image

`lib-fetcher-image` это библиотека Python для поиска изображений,
а так же получения на них ссылок в случае успеха с возможностью скачивания

## Установка из PyPI

```bash
pip install lib-fetcher-image
```

## Использование репозитория GitHub

```bash
git clone https://github.com/YuranIgnatenko/lib-fetcher-image.git
cd lib-fetcher-image
pip install .
```

## Пример использования

```bash
# импорт библиотеки
from lib_fetcher_image import FetchImage

# создание обьекта
fetcher_image = FetcherImage()

# параметры
pattern = "Море" # строка поиска (поддерживает: ru, en)
max_image = 2 # макс. кол-во ссылок в ответе в случае  успеха
# if max_image == -1 : возвращать все значения до конца
# else: вернуть столько же или меньше

# получение ссылок
list_urls = fetcher_image.get_images_urls(pattern, max_image)
# list_urls: ["http://../file.jpg", "http://../file.jpg"]

# скачивание файла по ссылке
fetcher_image.download(list_urls[0], "image.jpg")

# создание итератора используя
# строку запроса:  pattern
i = 0
for url in fetcher_image.search_iterator(pattern, max_image):
	print(f"{i}-{url}")
	i+=1

# создание итератора популярных изображений
i = 0
for url in fetcher_image.popular_iterator(max_image):
	print(f"{i}-{url}")
	i+=1


```

> using sources from site:
> `https://million-wallpapers.ru`
