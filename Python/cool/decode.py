from PIL import Image
filename = 'Starry Night By Vincent.png'
original = Image.open(filename)
filename = 'Starry Night By Vincent.jpg'
code = Image.open(filename)
filename = 'slate.png'
slate = Image.open(filename)
del filename

# Get the size of the image
width,height = original.size
pixels = slate.load()
originalPixels = original.load()
codedPixels = code.load()
# Process every pixel

for x in range(width):
    for y in range(height):
        if originalPixels[x,y][0]==codedPixels[x,y][0]:
            pixels[x,y]=(255,255,255,255)
        else:
            pixels[x,y]=(0,0,0,0)
slate.save('solved_message_1.png')
img = Image.open('solved_message_1.png')
img.show()

filename = 'slate.png'
slate = Image.open(filename)
pixels = slate.load()

for x in range(width):
    for y in range(height):
        if originalPixels[x,y][1]==codedPixels[x,y][1]:
            pixels[x,y]=(255,255,255,255)
        else:
            pixels[x,y]=(0,0,0,0)
slate.save('solved_message_2.png')
img = Image.open('solved_message_2.png')
img.show()

filename = 'slate.png'
slate = Image.open(filename)
pixels = slate.load()

for x in range(width):
    for y in range(height):
        if originalPixels[x,y][2]==codedPixels[x,y][2]:
            pixels[x,y]=(255,255,255,255)
        else:
            pixels[x,y]=(0,0,0,0)
slate.save('solved_message_3.png')
img = Image.open('solved_message_3.png')
img.show()

filename = 'slate.jpg'
slate = Image.open(filename)
pixels = slate.load()

for x in range(width):
    for y in range(height):
        if originalPixels[x,y]==codedPixels[x,y]:
            pixels[x,y]=(255,255,255,255)
        else:
            pixels[x,y]=(0,0,0,0)
slate.save('solved_message_mixed.png')
img = Image.open('solved_message_mixed.png')
img.show()
