#Takes in image and represents it in dots, 

from PIL import Image, ImageDraw, ImageFilter

GAP_BETWEEN_PIXEL_HORIZONTAL = 30
GAP_BETWEEN_PIXEL_VERTICAL = 20
MAX_DOT_SIZE = 20 # Maximum radius for dots
IMG_PATH = "IMG_20200630_190542.jpg" # Leave blank to be asked to input


#inputted ImageDraw, center (tuple x,y), color(greyscale 0-255), radius
def drawDot(imgDraw, center, color, radius):
	(x,y) = center
	imgDraw.ellipse([(x - radius, y - radius), (x + radius), (y + radius)] ,fill=color)



def main():
	global GAP_BETWEEN_PIXEL_HORIZONTAL, GAP_BETWEEN_PIXEL_VERTICAL, MAX_DOT_SIZE, IMG_PATH
	if (IMG_PATH == ""):
		IMG_PATH = input("Path: ")
	# Read in the image
	try:
		raw_img  = Image.open(IMG_PATH, mode='r')
	except IOError:
		print("Image not found")
		exit()

	#convert to greyscale  image
	img = raw_img.convert(mode = 'L') # 0 is black, 255 is white
	img = img.filter(ImageFilter.GaussianBlur(radius=3))
	px = img.load() # store the pixel map of the black and white image


	drawImg = Image.new('L', img.size, 255) # create all white image of the same size
	draw = ImageDraw.Draw(drawImg)

	for i in range(0, img.width, GAP_BETWEEN_PIXEL_HORIZONTAL):
		for j in range(0, img.height, GAP_BETWEEN_PIXEL_VERTICAL):
			drawDot(draw, (img.width - i, img.height - j), 0, MAX_DOT_SIZE * ((255 - px[i,j])/255) )

	drawImg.show()



if __name__ == "__main__":
    main()