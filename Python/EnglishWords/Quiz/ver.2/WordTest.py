import pygame
import random
from gtts import gTTS
import os
import time



英至中 = True




# Set Vars

pygame.init()
pygame.mixer.init()
pygame.font.init()
window = pygame.display.set_mode((500, 680))
pygame.display.set_caption("English Word Test")
rect = [
	pygame.Rect(130, 220, 0, 0).inflate(220, 160), 
	pygame.Rect(130, 400, 0, 0).inflate(220, 160), 
	pygame.Rect(370, 220, 0, 0).inflate(220, 160), 
	pygame.Rect(370, 400, 0, 0).inflate(220, 160), 
	pygame.Rect(130, 580, 0, 0).inflate(220, 160), 
	pygame.Rect(370, 580, 0, 0).inflate(220, 160), 
]
thisfont = lambda n:pygame.font.Font("msjh.ttc", n)
color = [(150, 150, 150) for i in range(6)]
accuracy = [1, 1]
timeBuffer = 0
combo = 0
score = 0




# Load Words

chinese = []
english = []
with open("EnglishWords.csv", encoding="utf-8") as file:
	if 英至中:
		for n, i in enumerate(file.read().split(",")):
			if n / 2 != n // 2:
				english.append(i)
			else:
				chinese.append(i)
	else:
		for n, i in enumerate(file.read().split(",")):
			if n / 2 == n // 2:
				english.append(i)
			else:
				chinese.append(i)
if 英至中:
	if not os.path.isdir('Assets'):
		os.mkdir("Assets")
	for word in chinese:
		if not os.path.isfile(f'Assets/{word}.mp3'):
			print(f"converting {word}")
			speech = gTTS(text = word, lang = "en", slow = False)
			speech.save(f'Assets/{word}.mp3')





# Shuffle Words

t = random.randint(0, len(english) - 1)
question = chinese[t]
randomNum1 = random.randint(0, len(english) - 1)
randomNum2 = random.randint(0, len(english) - 1)
while randomNum1 == randomNum2:
	randomNum2 = random.randint(0, len(english) - 1)
randomNum3 = random.randint(0, len(english) - 1)
while randomNum3 == randomNum2 or randomNum3 == randomNum1:
	randomNum3 = random.randint(0, len(english) - 1)
randomNum4 = random.randint(0, len(english) - 1)
while randomNum4 == randomNum2 or randomNum4 == randomNum1 or randomNum4 == randomNum3:
	randomNum4 = random.randint(0, len(english) - 1)
randomNum5 = random.randint(0, len(english) - 1)
while randomNum5 == randomNum2 or randomNum5 == randomNum1 or randomNum5 == randomNum3 or randomNum5 == randomNum4:
	randomNum5 = random.randint(0, len(english) - 1)
choice = [
	english[t], english[randomNum1], english[randomNum2], english[randomNum3], english[randomNum4], english[randomNum5]
]
random.shuffle(choice)





# Loop Start

run = True
while run:

	# See if mouse thoch the button
	collide = False
	point = pygame.mouse.get_pos()
	for n, i in enumerate(rect):
		collide = i.collidepoint(point)
		color[n] = (150, 150, 150) if collide else (200, 200, 200)


	# See if press space key
	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_SPACE] and 英至中:
		thisisasoundfile = pygame.mixer.music.load(f"Assets/{question}.mp3")
		pygame.mixer.music.play()



	# Check events
	for event in pygame.event.get():

		# Quit app
		if event.type == pygame.QUIT:
			# Show final score
			finalScore = thisfont(40).render(f"final score:{int(score)}", True, (0, 0, 0))
			finalAccuracy = thisfont(40).render(f"final accuracy:{round(100*accuracy[0]/accuracy[1], 2)}", True, (0, 0, 0))
			finalText = thisfont(40).render(f"{accuracy[0]}correct click/{accuracy[1]}clicks", True, (0, 0, 0))
			window.fill((255, 255, 255))
			window.blit(finalText, (250 - finalText.get_width() // 2, 70 - finalText.get_height() // 2))
			window.blit(finalAccuracy, (250 - finalAccuracy.get_width() // 2, 240 - finalAccuracy.get_height() // 2))
			window.blit(finalScore, (250 - finalScore.get_width() // 2, 380 - finalScore.get_height() // 2))
			pygame.display.update()
			pygame.time.delay(4000)
			run = False

		# Ckick the button
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			for n, i in enumerate(rect):
				collide = i.collidepoint(point)

				# Get the correct one
				if chinese.index(question) == english.index(choice[n]) and collide and timeBuffer == 0:


					# Re-shuffle the questions and selections
					t += 1
					if t == len(english):t %= len(english)
					try:question = chinese[t]
					except IndexError:run = False
					randomNum1 = random.randint(0, len(english) - 1)
					randomNum2 = random.randint(0, len(english) - 1)
					while randomNum1 == randomNum2:randomNum2 = random.randint(0, len(english) - 1)
					randomNum3 = random.randint(0, len(english) - 1)
					while randomNum3 == randomNum2 or randomNum3 == randomNum1:randomNum3 = random.randint(0, len(english) - 1)
					randomNum4 = random.randint(0, len(english) - 1)
					while randomNum4 == randomNum2 or randomNum4 == randomNum1 or randomNum4 == randomNum3:
						randomNum4 = random.randint(0, len(english) - 1)
					randomNum5 = random.randint(0, len(english) - 1)
					while randomNum5 == randomNum2 or randomNum5 == randomNum1 or randomNum5 == randomNum3 or randomNum5 == randomNum4:
						randomNum5 = random.randint(0, len(english) - 1)
					choice = [english[t], english[randomNum1], english[randomNum2], english[randomNum3], english[randomNum4], english[randomNum5]]
					random.shuffle(choice)
					thisisasoundfile = pygame.mixer.music.load(f"Assets/{question}.mp3")
					pygame.mixer.music.play()
					accuracy[0] += 1
					accuracy[1] += 1
					score += int(300 * round(1.1 ** combo, 2))
					combo += 1
					timeBuffer = 100
				elif collide and timeBuffer == 0:	
					accuracy[1] += 1
					combo = 0
					timeBuffer = 100
					thisisasoundfile = pygame.mixer.music.load("Assets/Wrong-answer-sound-effect.mp3")
					pygame.mixer.music.play()
					
				

	# Render
	Qtemp = thisfont(40).render(question, True, (0, 0, 0))
	Ctemp = [thisfont(20).render(i, 1, (0, 0, 0)) for i in choice]
	Atemp = thisfont(15).render(f'Accuracy:{round(100*accuracy[0]/accuracy[1], 2)}%', True, (0, 0, 0))
	scoreComboTemp = thisfont(15).render(f'Combo:{combo}    Score:{score}', True, (0, 0, 0))

	window.fill((255, 255, 255))
	for n, i in enumerate(rect):pygame.draw.rect(window, color[n], i)
	window.blit(Qtemp, (250 - Qtemp.get_width() / 2, 70 - Qtemp.get_height() / 2))
	window.blit(Atemp, (500 - Atemp.get_width() - 20, 20))
	window.blit(scoreComboTemp, (20, 20))
	for n, i in enumerate([(130, 220), (130, 400), (370, 220), (370, 400), (130, 580), (370, 580)]):window.blit(Ctemp[n], (i[0] - Ctemp[n].get_width()/2, i[1] - Ctemp[n].get_height()/2))
	pygame.display.update()
	timeBuffer -= 0 if timeBuffer == 0 else 1

pygame.quit()

# write in the record
if not os.path.isfile("Record.txt"):
	with open("Record.txt", "x"):pass
with open("Record.txt", "a+") as file:
	BACKSLASHN = '\n'
	file.write(f'{score}    {accuracy}       {round(score/accuracy[1], 2)}pts/clk      {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}{BACKSLASHN}')