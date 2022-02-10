from PIL import Image, ImageDraw
from io import BytesIO
from PyQt5.QtGui import QImage, QPixmap


def remove_end_spaces(string):
	return "".join(string.rstrip())

# Remove first and  end spaces
def remove_first_end_spaces(string):
	return "".join(string.rstrip().lstrip())

# Remove all spaces
def remove_all_spaces(string):
	return "".join(string.split())

# Remove all extra spaces
def remove_all_extra_spaces(string):
	return " ".join(string.split())

def add_corners(im, rad):
	circle = Image.new('L', (rad * 2, rad * 2), 0)
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
	alpha = Image.new('L', im.size, 255)
	w, h = im.size
	alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
	alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
	alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
	alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
	im.putalpha(alpha)
	return im

def make_rounded(pic):
	im = Image.open(BytesIO(pic))
	im = add_corners(im, 15)
	return pil2pixmap(im)

def pil2pixmap(image):
    bytes_img = BytesIO()
    image.save(bytes_img, format='png')

    qimg = QImage()
    qimg.loadFromData(bytes_img.getvalue())

    return QPixmap.fromImage(qimg)