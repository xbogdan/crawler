import requests
import lxml.html
from string import ascii_lowercase
from celery import Task
from .models import OnedenCategory, OnedenAliment
from django.conf import settings


class OnedenBaseTask(object):
	ENDPOINT = 'http://calorii.oneden.com'

	HEADERS = {
		'User-Agent': settings.REQUEST_UA,
		'Referer': ENDPOINT,
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding': 'gzip,deflate',
		'Accept-Language': 'en-US,en;q=0.8,ro;q=0.6,fr;q=0.4',
		'Cache-Control': 'max-age=0',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Origin': ENDPOINT
	}

	def get_base_cookie(self):
		cookies = {}
		first = requests.get(self.ENDPOINT, headers=self.HEADERS, verify=False, cookies=cookies)
		cookies.update(first.cookies.get_dict())

		return cookies


class CrawlOneden(Task, OnedenBaseTask):
	def run(self):
		base_cookie = self.get_base_cookie()

		alphabet = list(ascii_lowercase)
		nr = len(alphabet) - 1

		for i in range(0, nr):
			for j in range(0, nr):
				query = '{}{}'.format(alphabet[i], alphabet[j])
				print query

				params = {
					's': query
				}
				url = '{}/cauta/'.format(self.ENDPOINT)
				req = requests.get(url, headers=self.HEADERS, params=params, cookies=base_cookie, verify=False, allow_redirects=False)

				if req.status_code != 200:
					print req.url
					print req.status_code
					print req.content
					print 'Error'
					f = open('/Users/bogdanboamfa/crawler.txt', 'aw')
					f.write('query: {}, status code: {} \n'.format(query, req.status_code))
					f.close()
					continue

				self._process_search_table(req.content)

	@staticmethod
	def _process_search_table(content):
		html = lxml.html.fromstring(content)
		trs = html.cssselect('.tabelcalorii tr')

		for tr in trs:
			if len(tr.cssselect('th')) > 0:
				continue
			item = {}
			tds = tr.cssselect('td')
			if len(tds) < 8:
				continue

			item['group'] = tds[0].find('a')
			if item['group'] is not None:
				item['group'] = item['group'].text
				if item['group'] is not None:
					last_categ = item['group']
			else:
				item['group'] = last_categ

			item['name'] = tds[1].find('a').text
			item['calories'] = tds[2].text
			item['proteins'] = tds[3].text
			item['fats'] = tds[4].text
			item['carbohydrates'] = tds[5].text
			item['fibres'] = tds[6].text
			item['additional'] = tds[7].text

			if item['additional'] is None:
				item['additional'] = ''

			categ, created = OnedenCategory.objects.get_or_create(name=item['group'].lower())

			defaults = {
				'calories': item['calories'],
				'proteins': item['proteins'],
				'fats': item['fats'],
				'carbohydrates': item['carbohydrates'],
				'fibres': item['fibres'],
				'unit_quantity': 0.0,
				'additional': item['additional'],
			}

			aliment, created = OnedenAliment.objects.get_or_create(category=categ, name=item['name'], defaults=defaults)


class CrawlOnCategories(Task, OnedenBaseTask):
	def run(self):
		base_cookie = self.get_base_cookie()

		req = requests.get(self.ENDPOINT, headers=self.HEADERS, cookies=base_cookie, verify=False, allow_redirects=False)

		if req.status_code != 200:
			print req.status_code
			print req.content
			print 'Error'
			return

		html = lxml.html.fromstring(req.content)
		categs = html.cssselect('.tabel_categorie')

		for categ in categs:
			a = categ.cssselect('a')[0]
			name = a.text
			name = name.replace('Calorii ', '').lower()

			categories = name.split(" ")
			if len(categories) > 1:
				category_name = "{}-{}".format(categories[0], categories[1])
			else:
				category_name = categories[0]

			url = a.get('href')

			req = requests.get(url, headers=self.HEADERS, cookies=base_cookie, verify=False, allow_redirects=False)

			self._process_category_table(req.content, category_name)

	@staticmethod
	def _process_category_table(content, category):
		html = lxml.html.fromstring(content)
		trs = html.cssselect('.tabelcalorii tr')

		for tr in trs:
			if len(tr.cssselect('th')) > 0:
				continue
			item = {}
			tds = tr.cssselect('td')
			if len(tds) < 7:
				continue

			item['group'] = category
			item['name'] = tds[0].find('a').text
			item['calories'] = tds[1].text
			item['proteins'] = tds[2].text
			item['fats'] = tds[3].text
			item['carbohydrates'] = tds[4].text
			item['fibres'] = tds[5].text
			item['additional'] = tds[6].text

			if item['additional'] is None:
				item['additional'] = ''

			categ, created = OnedenCategory.objects.get_or_create(name=item['group'].lower())


			defaults = {
				'calories': item['calories'],
				'proteins': item['proteins'],
				'fats': item['fats'],
				'carbohydrates': item['carbohydrates'],
				'fibres': item['fibres'],
				'unit_quantity': 0.0,
				'additional': item['additional'],
			}

			aliment, created = OnedenAliment.objects.get_or_create(category=categ, name=item['name'], defaults=defaults)
