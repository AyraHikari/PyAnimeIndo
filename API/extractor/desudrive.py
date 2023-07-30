import requests

def desudrive(url):
	print("Bypass desudrive: " + url)
	return requests.get(url).url