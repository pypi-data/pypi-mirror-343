from setuptools import setup, find_packages

setup(
	name='lib-fetcher-image',
	version='1.4',
	packages=find_packages(),
	install_requires=[
		'requests',
		'beautifulsoup4',
		'fake_useragent',
		'Pillow',
	],
	description='Library for search and downloading images',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	author='Yurij',
	author_email='yuran.ignatenko@yanderx.ru',
	url='https://github.com/YuranIgnatenko/lib-fetcher-image',
)