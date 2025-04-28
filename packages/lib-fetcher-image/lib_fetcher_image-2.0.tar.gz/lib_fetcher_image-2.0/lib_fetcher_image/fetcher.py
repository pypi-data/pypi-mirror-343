from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO

class FetcherImage:
	def __init__(self):
		self._base_url  = "https://million-wallpapers.ru/"
		self._path_url_popular = "/oboi-na-rabochij-stol/"
		self._path_url_wallpapers = "/search-na-rabochij-stol/" 
		
		self._user_agent = UserAgent().random
		self._headers = {'User-Agent':self._user_agent}	
	
	def _pattern_to_prepare(self,pattern:str) -> str:
		return pattern.replace(" ","+").lower()

	def _build_path_url_search(self, pattern:str) -> str:
		pattern = self._pattern_to_prepare(pattern)
		return f"{self._base_url}{self._path_url_wallpapers}{pattern}/"

	def _build_path_url_popular(self) -> str:
		return f"{self._base_url}{self._path_url_popular}"

	def _build_path_url_page(self, pattern:str, page_number:int) -> str:
		return f"{self._build_path_url_search(pattern)}page-{page_number}/"
	
	def _build_path_url_page_popular(self, page_number:int) -> str:
		return f"{self._build_path_url_popular()}page-{page_number}/"

	def _build_path_url_image(self, link_image:str) -> str:
		return f"{self._base_url}{link_image}"

	def get_pages_count(self, pattern:str) -> int:
		'''returned count all pages: [0...)'''
		result = []
		url = self._build_path_url_search(pattern)
		response = requests.get(url=url, headers=self._headers)
		page = BeautifulSoup(response.content, 'html.parser')
		with open("test.html", "w", encoding='utf-8') as file: file.write(response.text)
		for link in page.find_all('a'):
			if str(link.get('href')).find('page-') != -1:
				result.append(self._build_path_url_image(link.get('href')))
		last_url_page = result[-1]
		return self._parse_number_page_from_url(last_url_page)

	def get_pages_urls(self, pattern:str) -> list[str]:
		result = []
		for i in range(self.get_pages_count(pattern)):
			result.append(self._build_path_url_page(pattern, i))
		return result
	
	
	def get_pages_popular_urls(self) -> list[str]:
		result = []
		for i in range(self.get_pages_popular()):
			result.append(self._build_path_url_page_popular(i))
		return result

	def get_pages_popular(self) -> int:
		'''returned count all pages: [0...)'''
		result = []
		url = self._build_path_url_popular()
		response = requests.get(url=url, headers=self._headers)
		page = BeautifulSoup(response.content, 'html.parser')
		with open("test.html", "w", encoding='utf-8') as file: file.write(response.text)
		for link in page.find_all('a'):
			if str(link.get('href')).find('page-') != -1:
				result.append(self._build_path_url_image(link.get('href')))
		last_url_page = result[-1]
		return self._parse_number_page_from_url(last_url_page)

	def _parse_number_page_from_url(self, url_page:str) -> int:
		'''"'https://some-url/pattern/page-6/' -> page-6 -> int(6)"'''
		return int(url_page.split("/")[-2].split('-')[-1])

	def get_images_urls(self, pattern:str, max_out:int=1) -> list[str]:
		'''returned list urls: ["http://...", "http://...", ...]
		default max_out == 1: returned first matched url
		if max_out == -1: returned all images urls
		else: (count returned urls) <= max_out (if matched success)  
		'''

		url = self._build_path_url_search(pattern)
		response = requests.get(url=url, headers=self._headers)
		page = BeautifulSoup(response.content, 'html.parser')

		result = []
		counter_urls = 0

		for link in page.find_all('a'):
			if str(link.get('href')).find('.jpg') != -1:
				counter_urls += 1
				result.append(self._build_path_url_image(link.get('href')))
				if counter_urls == max_out: break
		return result

	def search_iterator(self, pattern:str, max_out:int=-1):
		'''returned list urls: ["http://...", "http://...", ...]
		default max_out == -1
		if max_out == -1: returned all images urls
		else: (count returned urls) <= max_out (if matched success)  
		'''
		url = self._build_path_url_search(pattern)
		response = requests.get(url=url, headers=self._headers)
		page = BeautifulSoup(response.content, 'html.parser')

		counter = 0

		for url_page in self.get_pages_urls(pattern):
			response = requests.get(url=url_page, headers=self._headers)
			page = BeautifulSoup(response.content, 'html.parser')
			for link in page.find_all('a'):
				if (str(link.get('href')).find('.jpg') != -1):
					if counter == max_out:
						return
					else:
						counter += 1 
					yield self._build_path_url_image(link.get('href'))

	def popular_iterator(self, max_out:int=-1):
		'''returned list urls: ["http://...", "http://...", ...]
		default max_out == -1
		if max_out == -1: returned all images urls
		else: (count returned urls) <= max_out (if matched success)  
		'''
		url = self._build_path_url_popular()
		response = requests.get(url=url, headers=self._headers)
		page = BeautifulSoup(response.content, 'html.parser')

		counter = 0

		for i in range(self.get_pages_popular()):
			print(self._build_path_url_page_popular(i))
			response = requests.get(url=self._build_path_url_page_popular(i), headers=self._headers)
			page = BeautifulSoup(response.content, 'html.parser')
			for link in page.find_all('a'):
				if (str(link.get('href')).find('.jpg') != -1):
					if counter == max_out:
						return
					else:
						counter += 1 
					yield self._build_path_url_image(link.get('href'))

	def download(self, url:str, filename:str) -> bool:
		'''using filename example: my_file_image.jpg 
		format extension file: ".jpg" | ".jpeg"'''
		is_success = False
		try:
			response = requests.get(url)
			response.raise_for_status()
			image = Image.open(BytesIO(response.content))
			image.save(filename, 'JPEG')
			is_success = True
		except:
			is_success = False
		return is_success



