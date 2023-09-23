import requests
from bs4 import BeautifulSoup
from API.extractor.desudrive import desudrive

def getHost():
	response = requests.get('https://otakudesu.io/')
	soup = BeautifulSoup(response.text, features='html.parser')

	url_link = soup.find('a', {'id': 'skip'})
	if url_link:
		return url_link['href']
	else:
		raise Exception('Cannot find the host link')

host = getHost()

def getOngoing(next_page=1):
	data = BeautifulSoup(requests.get(host + f"ongoing-anime/page/{next_page}/").text, features="html.parser")
	ret = []

	animelists = data.find('div', {'class': 'venz'})
	for anime in animelists.findAll("li"):
		title = anime.find('h2', {"class": "jdlflm"}).text
		eps = anime.find('div', {"class": "epz"}).text
		img = anime.find('img')['src']
		hari = anime.find('div', {"class": "epztipe"}).text.strip()
		url = anime.find('a')['href']
		ret.append({"title": title, "eps": eps, "img": img, "hari": hari, "url": url})

	return ret


def getGenreList():
	r = BeautifulSoup(requests.get(host + "genre-list/").content, features="html.parser")
	genres = {}
	for data in r.find('ul', {"class": "genres"}).li.findAll("a"):
		genres[data.text] = data['href']
	return genres


def getGenreAnime(genre_path):
	r = BeautifulSoup(requests.get(host + genre_path).content, features="html.parser")
	data = []
	for anime in r.findAll('div', {"class": "col-anime"}):
		title = anime.find('div', {"class": "col-anime-title"}).text
		url = anime.find('div', {"class": "col-anime-title"}).a['href']
		eps = anime.find('div', {"class": "col-anime-eps"}).text
		img = anime.find('div', {"class": "col-anime-cover"}).img['src']
		data.append({"title": title, "eps": eps, "img": img, "hari": "", "url": url})
	return data


def getEpisodes(url):
	data = BeautifulSoup(requests.get(url).text, features="html.parser")
	ret = {'title': data.find('div', {"class": "jdlrx"}).text, 'cover': data.find('img', {'class': 'attachment-post-thumbnail'})['src'], 'sinopsis': "\n\n".join([x.text for x in data.find('div', {'class': 'sinopc'}).findAll('p')]), "info": "\n".join([x.text for x in data.find("div", {"class": "infozingle"}).findAll('p')]), "episodes": []}

	epslists = data.findAll('div', {'class': 'episodelist'})
	for chlists in epslists:
		for eps in chlists.findAll("li"):
			title = eps.find('a').text
			url = eps.find('a')['href']
			date = eps.find('span', {"class": "zeebr"}).text
			ret['episodes'].append({"title": title, "url": url, "date": date})

	ret['recommend'] = []
	recommendationData = data.find("div", {"class": "isi-recommend-anime-series"}).findAll("div", {"class": "isi-konten"})
	for reclist in recommendationData:
		title = reclist.span.text
		url = reclist.a['href']
		cover = reclist.img['src']
		ret['recommend'].append({"title": title, "url": url, "cover": cover})

	return ret


def getDownload(url):
	data = BeautifulSoup(requests.get(url).text, features="html.parser")
	ret = {}

	download = data.find('div', {'class': 'download'})
	if download:
		for dlurl in download.findAll("li"):
			filetype = dlurl.strong.text
			fileurl = ""
			for urlname in dlurl.findAll("a"):
				if "kfiles" in urlname.text.lower():
					fileurl = urlname['href']
					if "desudrive" in fileurl:
						fileurl = desudrive(fileurl)
			if not fileurl:
				fileurl = dlurl.a['href']
			ret[filetype] = fileurl
	elif batchlink := data.find('div', {'class': 'batchlink'}):
		for dlurl in batchlink.findAll("li"):
			filetype = dlurl.strong.text
			fileurl = ""
			for urlname in dlurl.findAll("a"):
				if "kfiles" in urlname.text.lower():
					fileurl = urlname['href']
					if "desudrive" in fileurl:
						fileurl = desudrive(fileurl)
			if not fileurl:
				fileurl = dlurl.a['href']
			ret[filetype] = fileurl

	return ret


def searchAnime(title):
	a = BeautifulSoup(requests.get(host + "/?s={}&post_type=anime".format(title)).content, features="html.parser")
	s = a.find("ul", {"class": "chivsrc"}).findAll("li")
	data = []
	for x in s:
		data.append({"title": x.h2.text, "img": x.img['src'], "url": x.h2.a['href']})
	
	return data
