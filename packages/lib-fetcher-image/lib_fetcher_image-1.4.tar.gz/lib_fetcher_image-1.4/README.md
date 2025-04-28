# lib-fetcher-image

`lib-fetcher-image` ��� ���������� Python ��� ������ �����������,
� ��� �� ��������� �� ��� ������ � ������ ������ � ������������ ����������

## ��������� �� PyPI

```bash
pip install lib-fetcher-image
```

## ������������� ����������� GitHub

```bash
git clone https://github.com/YuranIgnatenko/lib-fetcher-image.git
cd lib-fetcher-image
pip install .
```

## ������ �������������

```bash
# ������ ����������
from lib_fetcher_image import FetchImage

# �������� �������
fetcher_image = FetcherImage()

# ���������
pattern = "����" # ������ ������ (������������: ru, en)
max_image = 2 # ����. ���-�� ������ � ������ � ������  ������
# if max_image == -1 : ���������� ��� �������� �� �����
# else: ������� ������� �� ��� ������

# ��������� ������
list_urls = fetcher_image.get_images_urls(pattern, max_image)
# list_urls: ["http://../file.jpg", "http://../file.jpg"]

# ���������� ����� �� ������
fetcher_image.download(list_urls[0], "image.jpg")

# �������� ��������� ���������
# ������ �������:  pattern
i = 0
for url in fetcher_image.search_iterator(pattern, max_image):
	print(f"{i}-{url}")
	i+=1

# �������� ��������� ���������� �����������
i = 0
for url in fetcher_image.popular_iterator(max_image):
	print(f"{i}-{url}")
	i+=1


```

> using sources from site:
> `https://million-wallpapers.ru`
