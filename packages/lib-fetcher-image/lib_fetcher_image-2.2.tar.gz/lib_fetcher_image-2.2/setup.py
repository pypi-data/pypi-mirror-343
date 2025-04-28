from setuptools import setup, find_packages

setup(
	name='lib_fetcher_image',
	version='2.2',
	packages=find_packages(),
	install_requires=[
		'requests',
		'beautifulsoup4',
		'fake_useragent',
		'Pillow',
	],
	description='Library for search images',
	author='Yurij',
	author_email='yuran.ignatenko@yanderx.ru',
	url='https://github.com/YuranIgnatenko/lib_fetcher_image',
)