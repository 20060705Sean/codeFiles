from PIL import Image
'''
FILENAME = 'unknown (1).png'

image = Image.open(FILENAME)

width, height = image.size

image_rgba = image.convert("RGB")

color_array = []

for row in range(width):

	color_array.append([])

	for column in range(height):

		rgba_pixel_value = image_rgba.getpixel((row, column))

		color_array[row].append(rgba_pixel_value)

parsed_array = []

a = set()

for i in range(width):

	parsed_array.append([])

	for j in range(height):
		if color_array[i][j] != (133, 167, 221):
			a.add(color_array[i][j])
		else:
			parsed_array[i].append(' ')

'''

{}

'''
print(a)
#print("\n".join(list(map(lambda x:''.join(x), parsed_array))))

'''

image = Image.open('qwawdertwadayu.png')

imagecompared = Image.open('qwawdertyu.png')

width, height = image.size

image_rgba = image.convert("RGB")

imagecompared_rgba = imagecompared.convert("RGB")

image_store = imagecompared = Image.open('slater.png')
q = image_store.load()

color_array = []

for row in range(width):

	color_array.append([])

	for column in range(height):
		if imagecompared_rgba.getpixel((row, column))==(0, 0, 0):

			color_array[row].append('　')
			q[row, column] = (255,255, 255) if image_rgba.getpixel((row, column)) == (0, 0, 0) else(255, 255,255)
		else:

			color_array[row].append('Ｏ')
			q[row, column] = image_rgba.getpixel((row, column))
print("\n".join(list(map(lambda x:''.join(x), reversed(color_array)))))
image_store.save('qwawdertasadfwgadayu.png')
