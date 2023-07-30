import requests
from bs4 import BeautifulSoup

host = "https://krakenfiles.com"

def getId(url):
	return url.split("view/")[1].split("/file")[0]

def getStream(url):
	Id = getId(url)
	data = BeautifulSoup(requests.get(f"{host}/embed-video/{Id}").content, features="lxml")
	source = data.find("source")
	if source and source.get("src"):
		return "https:" + source.get("src")
	return ""