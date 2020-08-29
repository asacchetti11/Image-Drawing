#dots get larger if they are in a darker area
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

_GAP = 0.002
_BLUR = 6
_IMG_PATH = "mountain.jpg"
_MAX_DOT_SIZE = 10 # Maximum radius for dots

#spiral constants
a = 1.9
b = -3.6 #-1.1

def drawDot(imgDraw, center, color, radius):
	(x,y) = center
	imgDraw.ellipse([(x - radius, y - radius), (x + radius), (y + radius)] ,fill=color)

def func(t):
	#constants
	global a, b

	#actual function
	x = (a + b*t) * np.cos(t)
	y = (a + b*t) * np.sin(t)
	#return Point(x,y)
	return np.array([x, y])

#given an arclength solves for a time t on the given sprial
def arcLengthSolver(arclength):
	global a, b
	co = [(b**2)/3, a * b, b**2 + a**2, arclength * -1]
	for value in np.roots(co):
		if np.isreal(value):
			return value.real

def generateSpiral(img):
	global _GAP
	points = []
	i = 0
	while True: # creates points equidistant from eachother
		#point = func(arcLengthSolver(i)) + [img.width/2, img.height/2]
		point = func(i) + [img.width/2, img.height/2]

		x,y = tuple(point)
		if (x >= img.width and y >= img.height):
			break
		if (x < img.width and y < img.height):
			points.append(point)
		i = i + _GAP
		#drawDot(draw, point, 100, 1)
	#print(points,img.width*2)
	print("Sprial generated with {} points".format(len(points)))
	return points


def main():
	global _BLUR, _IMG_PATH

	if (_IMG_PATH == ""):
		_IMG_PATH = input("Path: ")
	# Read in the image
	try:
		raw_img  = Image.open(_IMG_PATH, mode='r')
	except IOError:
		print("Image not found")
		exit()

	#convert to greyscale  image
	img = raw_img.convert(mode = 'L') # 0 is black, 255 is white
	if (_BLUR > 0):
		img = img.filter(ImageFilter.GaussianBlur(radius=_BLUR))
	px = img.load() # store the pixel map of the black and white image

	points = generateSpiral(img)
	drawImg = Image.new('L', img.size, 255)
	draw = ImageDraw.Draw(drawImg)

	# draw a dot for each point based on darkness
	for p in points:
		i, j = tuple(p)
		drawDot(draw, p, 0, _MAX_DOT_SIZE*float(255 - px[i,j])/255 + 0.4 )

		#  = 1 - len(points)*subtraction
		#.4 - startinig/x= subtraction 

	drawImg.show()

if (__name__ == "__main__"):
    main()