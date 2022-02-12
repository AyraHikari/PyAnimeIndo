import json

def loadSettings():
	data = {}
	try:
		r = open("config.ini", "r")
		for l in r.read().split("\n"):
			if "=" in l:
				data[l.split("=")[0]] = l.split("=")[1]
	except FileNotFoundError:
		pass
	return data

def saveSettings(data):
	cfile = ""
	for l in data:
		cfile += "{}={}\n".format(l, data[l])
	w = open("config.ini", "w")
	w.write(cfile)
	w.close()
	return True


def loadData():
	data = {}
	try:
		r = open("data.json", "r")
		data = json.loads(r.read())
	except FileNotFoundError:
		pass
	except json.decoder.JSONDecodeError:
		pass
	return data

def saveData(data):
	w = open("data.json", "w")
	w.write(json.dumps(data))
	w.close()
	return True

def saveHistory(title):
	pass

def saveDataAnime(dataTitle, toSave):
	data = loadData()
	mydata = {}
	if data.get('saved'):
		mydata = data['saved']
	mydata[dataTitle] = eval(toSave)
	data['saved'] = mydata
	saveData(data)
	return True

def deleteDataAnime(toDel):
	data = loadData()
	mydata = []
	if data.get('saved'):
		mydata = data['saved']
	data['saved'].pop(toDel)
	saveData(data)
	return True

def getSavedAnime():
	data = loadData()
	return data['saved'] if data.get('saved') else {}

def getSavedAnimeList():
	data = loadData()
	if data.get("saved"):
		return [data['saved'][x] for x in data['saved']]
	return {}