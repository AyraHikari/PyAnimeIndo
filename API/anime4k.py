import requests, os
import zipfile


def download_url(url):
	print("Downloading: " + url)
	local_filename = url.split('/')[-1]
	# NOTE the stream=True parameter below
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(local_filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192): 
				f.write(chunk)
	return local_filename


def downloadAnime4K():
	print("Downloading packages...")
	fname = download_url(requests.get("https://api.github.com/repos/bloc97/Anime4K/releases/latest").json()['assets'][0]['browser_download_url'])
	print("Extracting...")
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
	try:
		os.remove(fname)
	except:
		pass


def writeLowA4K():
	print("Writing low config")
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


def writeHighA4K():
	print("Writing high config")
	LOW_END = '''CTRL+1 no-osd change-list glsl-shaders set "~~/shaders/Anime4K_Clamp_Highlights.glsl;~~/shaders/Anime4K_Restore_CNN_VL.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_VL.glsl;~~/shaders/Anime4K_AutoDownscalePre_x2.glsl;~~/shaders/Anime4K_AutoDownscalePre_x4.glsl;~~/shaders/Anime4K_Upscale_CNN_x2_M.glsl"; show-text "Anime4K: Mode A (HQ)"
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
	w.write(LOW_END)
	w.close()


def uninstallA4kdir():
	if os.name == "nt":
		try:
			os.remove("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\input.conf")
		except FileNotFoundError:
			pass
		x = os.listdir("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\shaders\\")
		for y in x:
			try:
				os.remove("C:\\Users\\" + os.environ['USERNAME'] + "\\AppData\\Roaming\\mpv\\shaders\\" + y)
			except FileNotFoundError:
				pass
	else:
		try:
			os.remove(f"/{os.getenv('HOME')}/.config/mpv/input.conf")
		except FileNotFoundError:
			pass
		x = os.listdir(f"/{os.getenv('HOME')}/.config/mpv/shaders")
		for y in x:
			try:
				os.remove(f"/{os.getenv('HOME')}/.config/mpv/shaders/" + y)
			except FileNotFoundError:
				pass
