import os
import random
import pygame
import sys
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

class PlayerDot(object):
	def __init__(self, win, positionStat, colour):
		self.win = win
		self.colour = colour
		self.image = pygame.Rect(positionStat[0], positionStat[1], 20, 20)
	def changePos(self, x, y):
		self.image.x, self.image.y = x, y
	def putOnScreenNow(self):
		pygame.draw.rect(self.win, self.colour, self.image)
class Player(object):
	def __init__(self, money, name):
		self.name = name
		self.money = money
		self.status = {}
		self.propiertary = []
		self.position = 0
		self.bankruptFlag = False
		super(Player, self).__init__()
	def __add__(self, other):self.money += other
	def __sub__(self, other):self.money -= other
	def affordable(self, price):return self.money >= price
	def move(self):
		if "Mortocycle" in self.status.keys():self.position = selectBlock()
		elif "inJail" not in self.status.keys():self.position += getRandom(1, 6)
	def statusReduction(self):
		for i in dict(self.status):
			self.status[i] -= 1
			if self.status[i] < 0:del self.status[i]
	def checkBlock(self):
		self.money = int(self.money)
		if "inJail" in self.status.keys():return True
		if self.position >= blockAmount:
		 	self.position %= blockAmount
		 	exec(blockInformation[0]["command"].replace("target", "players[self.name]"))
		currentBlockInfo = blockInformation[self.position]
		if currentBlockInfo["block-type"] == "normal":
			curPropiertary, curConstruction, curTolls = currentBlockInfo["propiertary"], currentBlockInfo["construction-price"], currentBlockInfo["tolls"]
			curHouses = curPropiertary.count("+")
			if curPropiertary == "" and purchaseQuery():
				if self.affordable(int(curConstruction[0])):
					self.money -= int(curConstruction[0]);blockInformation[self.position]["propiertary"] = self.name;self.propiertary.append(self.position)
				else:print("not Affordable")
			elif self.name in curPropiertary and purchaseQuery() and curHouses < 3:
				if self.affordable(int(curConstruction[curHouses])):
					self.money -= int(curConstruction[curHouses]);blockInformation[self.position]["propiertary"] += "+"
					nowBlock = currentBlockInfo["instance"]
					houze.append(House(window, "house", (nowBlock.x + 10 + 15 * curHouses, nowBlock.y + 30)))
				else:print("not Affordable")
			else:
				while not self.affordable(int(curTolls[curHouses])):
					if self.propiertary != []:
						block = selectBlock(condition = "self", propiertary = self.propiertary);HouseAmou = blockInformation[block]["propiertary"].count("+");self.money += int(blockInformation[block]["destruction-price"][HouseAmou]);blockInformation[block]["propiertary"] = "";self.propiertary.remove(block)
					else:
						self.bankruptFlag = True;print("bankrupt");break
				self.money -= int(curTolls[curHouses]);players[curPropiertary.replace("+", "")].money += int(curTolls[curHouses])
		elif currentBlockInfo["block-type"] == "special":
			curCommand = currentBlockInfo["command"];exec(curCommand.replace("target", "players[self.name]"))
class BlockObj(object):
	def __init__(self, win, name, filename, positionStat, isEdgeBlock, rotate):
		super(BlockObj, self).__init__()
		self.name = name
		self.win = win
		self.x, self.y = positionStat[0], positionStat[1]
		self.isEdgeBlock = isEdgeBlock
		self.image = pygame.image.load(f'Assets/{filename}.png')
		newScale = (int(self.image.get_width() * 0.25), int(self.image.get_height() * 0.25))
		self.image = pygame.transform.scale(self.image, newScale)
		self.image = pygame.transform.rotate(self.image, rotate)
	def putOnScreenNow(self):
		self.win.blit(self.image, (self.x, self.y))
class House(object):
	def __init__(self, win, filename, positionStat):
		super(House, self).__init__()
		self.win = win
		self.image = pygame.image.load(f'Assets/{filename}.png')
		newScale = (int(self.image.get_width() * 0.025), int(self.image.get_height() * 0.025))
		self.image = pygame.transform.scale(self.image, newScale)
		self.x, self.y = positionStat
	def putOnScreenNow(self):
		self.win.blit(self.image, (self.x, self.y))

width, height = 940, 940
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("GameName")
FPS = 60
rounds = 0
clock = pygame.time.Clock()
animationFlag = True
myFont = pygame.font.SysFont("comicsans", 40)

positionList = [
	(40, 40), (40 + 174, 40), (40 + 174 + 128, 40), 
	(40 + 174 + 128*2, 40), (40 + 174 + 128*3, 40), (40 + 174 + 128*4, 40), 
	(40 + 174 + 128*4, 40 + 174), (40 + 174 + 128*4, 40 + 174 + 128), 
	(40 + 174 + 128*4, 40 + 174 + 128*2), (40 + 174 + 128*4, 40 + 174 + 128*3), (40 + 174 + 128*4, 40 + 174 + 128*4), 
	(40 + 174 + 128*3, 40 + 174 + 128*4), (40 + 174 + 128*2, 40 + 174 + 128*4), (40 + 174 + 128, 40 + 174 + 128*4), 
	(40 + 174, 40 + 174 + 128*4), (40, 40 + 174 + 128*4), 
	(40, 40 + 174 + 128*3), (40, 40 + 174 + 128*2), (40, 40 + 174 + 128), (40, 40 + 174)]
rotater = [
	180, 180, 180, 180, 180, 
	90, 90, 90, 90, 90, 
	0, 0, 0, 0, 0, 
	270, 270, 270, 270, 270]
			
# Incomplete
def purchaseQuery():
	return True
def selectBlock(condition = "any", propiertary = []):
	return getRandom(0, blockAmount) if condition == "any" else propiertary[random.randint(0, len(propiertary) - 1)]


size, blockInformation, players = tuple(), dict(), dict()
with open("classic.mon") as file:
	'''
	When editing a map, make sure there are 2(length + width) + 4 blocks
	length  width
	special  name  command
	normal  name  build  tolls  crush
	'''
	size = tuple(file.readline()[:-1].split("  "))
	file.readline()
	for i, line in enumerate(file.readlines()):
		temp = line[:-1].split("  ")
		if temp[0] == "normal":blockInformation[i] = {"instance" : BlockObj(window, temp[1], temp[1], positionList[i], bool(temp[5]), rotater[i]), "name" : temp[1], "block-type" : temp[0], "propiertary" : "", "construction-price" : temp[2].split(" "), "tolls" : temp[3].split(" "), "destruction-price" : temp[3].split(" ")}
		elif temp[0] == "special":blockInformation[i] = {"instance" : BlockObj(window, temp[1], temp[1], positionList[i], bool(temp[3]), rotater[i]), "name" : temp[1], "block-type" : temp[0], "command" : temp[2]}
playerNames = ["Tom", "Dick", "Harry", "Danny"]
blockAmount, playerAmount = len(blockInformation), len(playerNames)
getRandom = lambda a, b:random.randint(a, b)
random.shuffle(playerNames)
for n in playerNames:players[n] = Player(5000, n)

dots = {
	0 : PlayerDot(window, (45, 45), (getRandom(0, 255), getRandom(0, 255), getRandom(0, 255))), 
	1 : PlayerDot(window, (65, 45), (getRandom(0, 255), getRandom(0, 255), getRandom(0, 255))), 
	2 : PlayerDot(window, (45, 65), (getRandom(0, 255), getRandom(0, 255), getRandom(0, 255))), 
	3 : PlayerDot(window, (65, 65), (getRandom(0, 255), getRandom(0, 255), getRandom(0, 255))), }
houze = []

while True:
	window.fill((0, 0, 0))
	if not animationFlag:
		nowPlayer = playerNames[int(rounds)]
		players[nowPlayer].statusReduction()
		players[nowPlayer].move()
		players[nowPlayer].checkBlock()
		rounds = (rounds + 1) % (len(playerNames))

		adder = [(5, 5), (5, 25), (25, 5), (25, 25)][rounds]
		nowPos = positionList[players[nowPlayer].position]
		dots[rounds].changePos(nowPos[0] + adder[0], nowPos[1] + adder[1])
		if players[nowPlayer].bankruptFlag == True:
	 		playerNames.remove(nowPlayer)
		animationFlag = True
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()


		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				animationFlag = False
	#keys_pressed = pygame.key.get_pressed()
	#if keys_pressed[K_SPACE]:
		#animationFlag = False


	for i in blockInformation:
		blockInformation[i]["instance"].putOnScreenNow()
	for i in dots:
		dots[i].putOnScreenNow()
	for i in houze:
		i.putOnScreenNow()

	c = 0
	posC = [(10, 10), (750, 920), (10, 920), (750, 10)] 
	for i in players:
		draw_text = myFont.render(f'{players[i].name}:${players[i].money if players[i].money >= 0 else "BANKRUPT"}', 1, (255, 255, 255))
		window.blit(draw_text, (posC[c][0], posC[c][1]))
		c += 1
	pygame.display.update()
	clock.tick(FPS)

	
	
	
 