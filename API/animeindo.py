#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import requests
import shutil
import struct
import time
import subprocess as subp
import zipfile

#import py7zr

from bs4 import BeautifulSoup
from .zdl import zdl
#from pyDownload import Downloader

try:
	import distro
except ModuleNotFoundError:
	pass

VERSION = "v1.0.1"


def is64Bit():
	if (8 * struct.calcsize("P")) == 64:
		return True
	return False

def clear():
	return
	if os.name == 'nt':
		os.system("cls")
	else:
		os.system("clear")

def download_url(url):
	downloader = Downloader(url=url)
	return downloader.file_name

def splashInit():
	data = """
  _____                      _                _____           _       
 |  __ \\         /\\         (_)              |_   _|         | |      
 | |__) |   _   /  \\   _ __  _ _ __ ___   ___  | |  _ __   __| | ___  
 |  ___/ | | | / /\\ \\ | '_ \\| | '_ ` _ \\ / _ \\ | | | '_ \\ / _` |/ _ \\ 
 | |   | |_| |/ ____ \\| | | | | | | | | |  __/_| |_| | | | (_| | (_) |
 |_|    \\__, /_/    \\_\\_| |_|_|_| |_| |_|\\___|_____|_| |_|\\__,_|\\___/ 
         __/ |                                                        
        |___/                                                         
"""
	print(data)

def DownloadOnlineMPV(is64Bit):
	if os.name == 'nt':
		dl = "https://sourceforge.net/projects/mpv-player-windows/files/" + ("64bit/" if is64Bit else "32bit/")
		sup = BeautifulSoup(requests.get(dl).content, features="html.parser")
		fname = sup.find('th', {"headers": "files_name_h"}).span.text
		url = "https://jaist.dl.sourceforge.net/project/mpv-player-windows/" + ("64bit/" if is64Bit else "32bit/") + "/" + fname
		print("Downloading MPV...")
		fname = download_url(url)
		print("Extracting MPV...")
		archive = py7zr.SevenZipFile(fname, mode='r')
		archive.extractall(path=".")
		archive.close()
	else:
		chk = distro.id()
		if chk.lower() == "ubuntu":
			os.system("sudo apt install mpv")
		elif chk.lower() == "arch":
			os.system("sudo pacman -S mpv")
		else:
			print("Distro tidak diketahui, cobalah install mpv secara manual")
			print("https://mpv.io/installation/")
			time.sleep(5)
	print("Done")
	time.sleep(2)
	clear()

def doInstallMPV():
	print("MPV tidak tersedia, apakah anda ingin mengunduh MPV?")
	print("Y = Ya; N = Tidak; P = Gunakan MPV pada path custom")
	i = input("[Y/N/P]: ")
	if i.lower() == "y":
		DownloadOnlineMPV(is64Bit())
	elif i.lower() == "p":
		path = input("Masukan path MPV: ")
		curr = [x.split(".")[0] for x in os.listdir(path)]
		if "mpv" not in curr:
			doInstallMPV()
		else:
			w = open("mpv_path.txt", "w")
			w.write(str(path))
			w.close()
	else:
		return

def checkMPV():
	if os.name == 'nt':
		curr = [x.split(".")[0] for x in os.listdir()]
		if "mpv" not in curr and "mpv_path" not in curr:
			doInstallMPV()
			mainMenu()
	else:
		try:
			a = subp.Popen(['which', 'mpv'], stdout=subp.DEVNULL, stderr=subp.STDOUT).wait()
		except FileNotFoundError:
			doInstallMPV()
			mainMenu()
		if a != 0:
			doInstallMPV()
			mainMenu()

def get_main():
	url = "https://otakudesu.pro/ongoing-anime/"
	data = BeautifulSoup(requests.get(url).text, features="html.parser")
	ret = []

	animelists = data.find('div', {'class': 'venz'})
	for anime in animelists.findAll("li"):
		title = anime.find('h2', {"class": "jdlflm"}).text
		eps = anime.find('div', {"class": "epz"}).text
		img = anime.find('img')['src']
		url = anime.find('a')['href']
		ret.append({"title": title, "eps": eps, "img": img, "url": url})

	return ret

def get_episodes(url):
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

def get_download(url):
	data = BeautifulSoup(requests.get(url).text, features="html.parser")
	ret = {}

	download = data.find('div', {'class': 'download'})
	for dlurl in download.findAll("li"):
		filetype = dlurl.strong.text
		fileurl = ""
		for urlname in dlurl.findAll("a"):
			if "zippyshare" in urlname.text.lower():
				fileurl = urlname['href']
		if not fileurl:
			fileurl = dlurl.a['href']
		ret[filetype] = fileurl

	return ret

def is4KAvaiable():
	if os.name == 'nt':
		try:
			shaders = os.listdir("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\shaders")
		except FileNotFoundError:
			shaders = []
		if "Anime4K" in [x.split("_")[0] for x in shaders]:
			return True
	else:
		try:
			shaders = os.listdir(f"/{os.getenv('HOME')}/.config/mpv/shaders")
		except FileNotFoundError:
			shaders = []
		if "Anime4K" in [x.split("_")[0] for x in shaders]:
			return True
	return False

def renderLatest():
	clear()
	print("Anime Terbaru Subtitle Indonesia")
	c = 0
	main = get_main()
	for anime in main:
		c += 1
		print("{}. {} ({})".format(c, anime['title'], anime['eps']))

	print(" ")
	print("[M = Main menu]")
	i = input("Pilih anime: ")
	if i.lower() == "m":
		mainMenu()
	elif str(i).isdigit():
		renderEps(main[int(i)-1]['url'])

def renderEps(url):
	clear()
	epsdata = get_episodes(url)
	print(epsdata['title'])
	if epsdata['sinopsis']:
		print(" ")
		print(epsdata['sinopsis'])
	print(" ")
	c = 0
	for eps in epsdata['episodes']:
		c += 1
		print("{}. {} ({})".format(c, eps['title'], eps['date']))
	print(" ")
	print("[M = Main menu]")
	i = input("Pilih episode: ")
	if i.lower() == "m":
		mainMenu()
	elif str(i).isdigit():
		renderDownload(epsdata['episodes'][int(i)-1]['url'], epsdata['episodes'][int(i)-1]['title'], url)

def renderDownload(url, title, origurl):
	clear()
	print(title)
	data = BeautifulSoup(requests.get(url).text, features="html.parser")
	ret = {}

	download = data.find('div', {'class': 'download'})
	for dlurl in download.findAll("li"):
		filetype = dlurl.strong.text
		fileurl = ""
		for urlname in dlurl.findAll("a"):
			if "zippyshare" in urlname.text.lower():
				fileurl = urlname['href']
		if not fileurl:
			fileurl = dlurl.a['href']
		ret[filetype] = fileurl

	c = 0
	for res in ret:
		c += 1
		print("{}. {}".format(c, res))
	print(" ")
	print("[M = Main menu]")
	i = input("Pilih resolusi: ")
	if i.lower() == "m":
		mainMenu()
	elif str(i).isdigit():
		streamingAnime(ret[list(ret)[int(i)-1]], title, list(ret)[int(i)-1], origurl)

def streamingAnime(url, title, quality, origurl):
	clear()
	print(title)
	print("Resolusi: " + quality)
	print("Sebentar ya...")
	zdirect = zdl(url)

	try:
		custpath = open("mpv_path.txt", "r").read()
	except FileNotFoundError:
		custpath = False
	if custpath:
		subp.check_call(str(custpath + "\\mpv " + zdirect), shell=True)
	else:
		subp.check_call(str("mpv " + zdirect), shell=True)
	time.sleep(3)
	renderEps(origurl)

def downloadAnime4K():
	clear()
	print("Downloading packages...")
	fname = download_url(requests.get("https://api.github.com/repos/bloc97/Anime4K/releases/latest").json()['assets'][0]['browser_download_url'])
	if os.name == "nt":
		try:
			shaders = os.mkdir("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv")
		except FileExistsError:
			pass
		try:
			shaders = os.mkdir("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\shaders")
		except FileExistsError:
			pass
		with zipfile.ZipFile(fname, 'r') as zip_ref:
			zip_ref.extractall("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\shaders\\")
	else:
		try:
			shaders = os.mkdir(f"/{os.getenv('HOME')}/.config")
		except FileExistsError:
			pass
		try:
			shaders = os.mkdir(f"/{os.getenv('HOME')}/.config/mpv")
		except FileExistsError:
			pass
		try:
			shaders = os.mkdir(f"/{os.getenv('HOME')}/.config/mpv/shaders")
		except FileExistsError:
			pass
		with zipfile.ZipFile(fname, 'r') as zip_ref:
			zip_ref.extractall(f"/{os.getenv('HOME')}/.config/mpv/shaders")
	setupAnime4K()

def setupAnime4K():
	clear()
	print("\n[L = Low: Cocok untuk VGA low-end seperti RX 570 keatas]")
	print("\n[H = High: Cocok untuk VGA high-end seperti RTX 3060 keatas]")
	print("\n[X = Lewati setup, jika belum di setup ketik 'K' pada main menu]")
	i = input("Pilih preset: ")
	if i.lower() == "l":
		LOW_END = '''CTRL+1 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_M.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"; show-text "Anime4K: Mode A (Fast)"
CTRL+2 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_Soft_M.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"; show-text "Anime4K: Mode B (Fast)"
CTRL+3 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Upscale_Denoise_CNN_x2_M.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"; show-text "Anime4K: Mode C (Fast)"
CTRL+4 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_M.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl;~~/shaders/Anime4K_Restore_CNN_S.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"; show-text "Anime4K: Mode A+A (Fast)"
CTRL+5 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_Soft_M.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Restore_CNN_Soft_S.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"; show-text "Anime4K: Mode B+B (Fast)"
CTRL+6 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Upscale_Denoise_CNN_x2_M.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Restore_CNN_S.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_S.glsl"; show-text "Anime4K: Mode C+A (Fast)"

CTRL+0 no-osd change-list glsl-shaders clr ""; show-text "GLSL shaders cleared"'''
		if os.name == "nt":
			w = open("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\input.conf", "w")
		else:
			w = open(f"/{os.getenv('HOME')}/.config/mpv/input.conf", "w")
		w.write(LOW_END)
		w.close()
	elif i.lower() == "h":
		HIGH_END = '''CTRL+1 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_VL.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_VL.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"; show-text "Anime4K: Mode A (HQ)"
CTRL+2 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_Soft_VL.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_VL.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"; show-text "Anime4K: Mode B (HQ)"
CTRL+3 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Upscale_Denoise_CNN_x2_VL.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"; show-text "Anime4K: Mode C (HQ)"
CTRL+4 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_VL.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_VL.glsl;~~/shaders/Anime4K_Restore_CNN_M.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"; show-text "Anime4K: Mode A+A (HQ)"
CTRL+5 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_Soft_VL.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_VL.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Restore_CNN_Soft_M.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"; show-text "Anime4K: Mode B+B (HQ)"
CTRL+6 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Upscale_Denoise_CNN_x2_VL.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Restore_CNN_M.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"; show-text "Anime4K: Mode C+A (HQ)"

CTRL+0 no-osd change-list glsl-shaders clr ""; show-text "GLSL shaders cleared"'''
		if os.name == "nt":
			w = open("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\input.conf", "w")
		else:
			w = open(f"/{os.getenv('HOME')}/.config/mpv/input.conf", "w")
		w.write(HIGH_END)
		w.close()
	elif i.lower() == "x":
		print("Setup di lewati...")
	else:
		setupAnime4K()
	time.sleep(2)
	mainMenu()

def searchAnimeX(title):
	clear()
	print("Pencarian dari '{}'".format(title))
	a = BeautifulSoup(requests.get("https://otakudesu.pro/?s={}&post_type=anime".format(title)).content, features="html.parser")
	s = a.find("ul", {"class": "chivsrc"}).findAll("li")
	c = 0
	for x in s:
		c += 1
		print("{}. {}".format(c, x.h2.text))

	print("\n[M = Main menu]")
	i = input("\nPilih anime: ")
	if i.lower() == "m":
		mainMenu()
	elif str(i).isdigit():
		renderEps(s[int(i)-1].h2.a['href'])

def searchAnime(title):
	a = BeautifulSoup(requests.get("https://otakudesu.pro/?s={}&post_type=anime".format(title)).content, features="html.parser")
	s = a.find("ul", {"class": "chivsrc"}).findAll("li")
	data = []
	for x in s:
		data.append({"title": x.h2.text, "img": x.img['src'], "url": x.h2.a['href']})
	
	return data

def mainMenu():
	clear()
	splashInit()
	checkMPV()
	is4k = is4KAvaiable()
	print("1. Cek anime terbaru")
	print("2. Cari anime")
	print(" ")
	if not is4k:
		print("K. (opsional) Install Anime 4K filter")
		print(" ")

	i = input("Pilih masukan: ")
	if i == "1":
		renderLatest()
	elif i == "2":
		s = input("Ketik judul anime: ")
		searchAnime(s)
	elif i.lower() == "k":
		downloadAnime4K()

def checkUpdate():
	data = requests.get("https://api.github.com/repos/AyraHikari/PyAnimeIndo/releases/latest").json()
	if data['tag_name'] != VERSION:
		i = input("Versi baru tersedia ({}), update sekarang? [Y/N]: ".format(data['tag_name']))
		if i.lower() == 'y':
			return webbrowser.open("https://github.com/AyraHikari/PyAnimeIndo/releases")
	return False
	data = requests.get("https://api.github.com/repos/AyraHikari/PyAnimeIndo/releases/latest").json()
	if data['tag_name'] != VERSION:
		i = input("Versi baru tersedia ({}), update sekarang? [Y/N]: ".format(data['tag_name']))
		if i.lower() == 'y':
			print("Downloading...")
			if "nt" in os.name:
				dl = [x['browser_download_url'] for x in data['assets'] if "windows" in x['name'].lower()][0]
			else:
				dl = [x['browser_download_url'] for x in data['assets'] if "linux" in x['name'].lower()][0]
			fname = download_url(dl)
			print("Extracting...")
			with zipfile.ZipFile(fname, 'r') as zip_ref:
				zip_ref.extractall(".")
			print("Update selesai")
			time.sleep(3)

if __name__ == "__main__":
	clear()
	checkUpdate()
	mainMenu()
