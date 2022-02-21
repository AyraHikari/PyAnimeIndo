import requests
from bs4 import BeautifulSoup

host = "https://otakudesu.pro/"

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
