import requests

SIZE = 500
REGION = 65

FILE_NAME = 'news.json'

URL_NEWS = 'https://xn--90adear.xn--p1ai/news/region?perPage={}&page={}&region={}'
HEADER_OWN = {
	'Content-Type': 'application/json',
	'X-Requested-With': 'xmlhttprequest'
}

URL_ITEM = 'https://xn--90adear.xn--p1ai/r/65/news/item/{}?ajax=1'

ITEM_IDS = []
ITEMS = []

PRE_PAGE, PAGE = 0, 1
while True:
	URL = URL_NEWS.format(SIZE, PAGE, REGION)
	r = requests.get(URL, headers=HEADER_OWN)
	ans = r.json()
	if ans['paginator']['page'] == PRE_PAGE:
		break
	for i in ans['data']:
		info = {
			'id': i['id'],
			'title': i['title'],
			'img': i['image'],
			'ts': i['datetime'],
			'reg_code': i['region']['code'],
			'reg_name': i['region']['name']
		}
		ITEM_IDS.append(info)
	print('Получена страница №{}'.format(PAGE))
	PRE_PAGE = PAGE
	PAGE += 1


f = open(FILE_NAME, 'ab')

k = 1
for j in ITEM_IDS:
	print('Обработано {} страниц'.format(k))
	URL = URL_ITEM.format(j['id'])
	r = requests.get(URL, headers=HEADER_OWN)
	item = r.json()
	dop_info = {
		'description': item['data']['description'],
		'text': item['data']['text'],
		'docs': [p['url'] for p in item['data']['documents']]
	}
	j.update(dop_info)
	f.write((str(j) + '\n').encode('utf-8'))
	k += 1


f.close()
