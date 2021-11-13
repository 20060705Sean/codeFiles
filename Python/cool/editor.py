from PIL import Image

FILENAME = 'The Scream.jpg'

image = Image.open(FILENAME)

image_rgb = image.convert("RGB")

print(image_rgb.getpixel((130, 130)))

FILENAME = 'The Screamed.jpg'

image = Image.open(FILENAME)

image_rgb = image.convert("RGB")

print(image_rgb.getpixel((130, 130)))

FILENAME = 'Is it screaming.jpg'

image = Image.open(FILENAME)

pixel = image.load()

pixel[130, 130] = (158, 230, 170)

image.save('monalisa1.jpg')