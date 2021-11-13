from PIL import Image
image = {
	"base" : {
		'image' : (im := Image.open('ori.png')), #input("Base image name:"))
		'pixel' : im.load(),
		'rgb' : im.convert('RGB'),  
		'size' : im.size
	}, 
	"message" : {
		'image' : (im := Image.open('下載.png')), #input("Message image name:"))
		'pixel' : im.load(), 
		'rgb' : im.convert('RGB'), 
		'size' : im.size
	}
}
for i in range(image['base']['size'][0]):
	for j in range(image['base']['size'][1]):
		if i > image['message']['size'][0] - 1 or j > image['message']['size'][1] - 1:
			continue
		now_ori = image['base']['rgb'].getpixel((i, j))
		now_msg = image['message']['rgb'].getpixel((i, j))
		
		if now_msg != (255, 255, 255):
			print(now_msg, end = ' ')
			image['base']['pixel'][i, j] = (255, 255, 255) if now_ori == (0, 0, 0) else (0, 0, 0)#(now_ori[0] + 1, now_ori[1], now_ori[2])#tuple([(now_ori[t] + now_msg[t]) % 256 for t in range(3)])
image['base']['image'].save('enc.png')#input("Encoded image name:"))


