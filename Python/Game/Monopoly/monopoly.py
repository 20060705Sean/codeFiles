import os
import sys
import random
import pygame
from pygame.locals import *
pygame.font.init()
class mod_mapFileReader(object):
	def __init__(self, mapFilename):
		super(mod_mapFileReader, self).__init__()
		# Parse
		with open(mapFilename) as file:
			self.map_version = mapFilename.split(".")[1]
			self.blk_information = dict()
			if self.map_version == "mon":
				self.blk_amount = 4 + 2 * sum(list(map(int, file.readline().split())))
				self.img_folderName = file.readline()[:-1]
				readOneImageFlag = False
				for i, line in enumerate(file.readlines()):
					line = line[:-1].split("  ")
					if line[0] == "normal":
						self.blk_information[i] = {
							"block-type" : line[0], 
							"block-name" : line[1], 
							"block-purchase-price" : list(map(int, line[2].split())), 
							"block-tolls" : list(map(int, line[3].split())), 
							"block-sell-price" : list(map(int, line[4].split())),
							"is-edge-block" : bool(line[5]), 
							"image-file-position" : f"{os.path.join(self.img_folderName, line[1])}.png"
						}
						if not readOneImageFlag:
							img = pygame.image.load(f"{os.path.join(self.img_folderName, line[1])}.png")
							self.blk_size = (img.get_width(), img.get_height())
					else:
						self.blk_information[i] = {
							"block-type" : line[0], 
							"block-name" : line[1], 
							"command" : line[2], 
							"image-file-position" : f"{os.path.join(self.img_folderName, line[1])}.png", 
							"is-edge-block" : bool(line[3])
						}
		# Command
		self.getBlocksInformation = lambda:self.blk_information
		self.getBlockAmount = lambda:self.blk_amount
		self.getMapVersion = lambda:self.map_version
class mod_coordinateCalculator(object):
	'''
	screenArguments   {size  (x, y), align, margin}
	blocksArguments   {mod_mapFileReader.blk_size, mod_mapFileReader.blk_amount}
	'''
	def __init__(self, screenArguments, blocksArguments):
		super(mod_coordinateCalculator, self).__init__()
		# Read
		scr_width, scr_height = screenArguments["size"]
		scr_align = {"left" : 0, "center" : 1}[screenArguments["align"]]
		scr_margin = screenArguments["margin"]
		blk_width, blk_height = blocksArguments["size"]
		blk_amount = blocksArguments["amount"]
		# Compute
		scr_availableWidth = scr_width - scr_margin * 2 
		scr_availableHeight = scr_height - scr_margin * 2
		if blk_amount % 4 == 0:blk_blockPerSide = blk_amount // 4 + 1
		else:raise AttributeError(f"Block amounts must be 4x+1 but got {blk_amount}")
		self.blk_scale = (
			round(scr_availableWidth / (2 * blk_height + (blk_blockPerSide - 2) * blk_width), 3), 
			round(scr_availableHeight / (2 * blk_height + (blk_blockPerSide - 2) * blk_width), 3)
		)
		blk_actualWidth = blk_width * self.blk_scale[0]
		blk_actualHeight = blk_height * self.blk_scale[1]
		temp_p, temp_q = blk_blockPerSide, blk_blockPerSide - 1
		self.blk_positions = lambda align = scr_align:[
			(
				int(scr_margin + blk_actualHeight // 2 * {True : 1, False : 0}[i % temp_q == 0] * align + blk_actualWidth // 2 * {True : 0, False : 1}[i % temp_q == 0] * align + blk_actualHeight * {True : 1, False : 0}[0 < i < 3 * temp_q] + blk_actualWidth * {0 : (i - 1) if i != 0 else 0, 1 : temp_p - 2, 2 : temp_p - 2 - i % temp_q, 3 : 0}[int(i // temp_q)]), 
				int(scr_margin + blk_actualHeight // 2 * {True : 1, False : 0}[i % temp_q == 0] * align + blk_actualWidth // 2 * {True : 0, False : 1}[i % temp_q == 0] * align + blk_actualHeight * {True : 1, False : 0}[temp_p <= i] + blk_actualWidth * {0 : 0, 1 : i - temp_q - 1 if i - temp_q > 0 else 0, 2 : temp_p - 2, 3 : temp_p - 2 - i % temp_q}[int(i // temp_q)])
			)
			for i in range(blk_amount)
		]
		# Command
		self.__getShiftedPositions = lambda pos, n:pos[-n:] + pos[:-n]
		self.__getReversedPositions = lambda mode, align:self.blk_positions(align) if mode == "clockwise" else self.__getShiftedPositions(list(reversed(self.blk_positions(align))), 1)
		self.getPositions = lambda shift = 0, direction = "clockwise", align = 1:self.__getShiftedPositions(self.__getReversedPositions(direction, align), shift)
		self.getRotaters = lambda shift = 0, direction = "clockwise":self.__getShiftedPositions(list(reversed([[180, 90, 0, 270][i // (blk_blockPerSide - 1)] for i in range(blk_amount)]) if direction != "clockwise" else [[180, 90, 0, 270][i // (blk_blockPerSide - 1)] for i in range(blk_amount)]), -shift)
		self.getScale = lambda:self.blk_scale
class obj_block(object):
	'''
	adhesionFrame      pygame.display
	blockInformation   (index, mod_mapFileReader.getBlocksInformation())
	imageInformation   {grid-position  (align = left), scale, rotate}
	'''
	def __init__(self, adhesionFrame, blockInformation, imageInformation):
		# Extract Argument
		super(obj_block, self).__init__()
		self.adhesionFrame = adhesionFrame
		self.index = blockInformation[0]
		blockInformation = blockInformation[1]

		self.category = blockInformation["block-type"]
		self.name = blockInformation["block-name"]
		if self.category == "special":self.command = blockInformation["command"]
		else:
			self.purchasePrice = blockInformation["block-purchase-price"]
			self.tolls = blockInformation["block-tolls"]
			self.sellPrice = blockInformation["block-sell-price"]
			self.propiertary = ""
			self.houses = 0
		# Read Image
		self.image = pygame.image.load(blockInformation["image-file-position"])
		self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * imageInformation["scale"][0]), int(self.image.get_height() * imageInformation["scale"][1])))
		self.image = pygame.transform.rotate(self.image, imageInformation["rotate"])
		self.img_position = imageInformation["grid-position"]
		# Command
		self.showOnScreen = lambda:self.adhesionFrame.blit(self.image, self.img_position)
class obj_player(object):
	'''
	adhesionFrame      pygame.display
	order              int
	imageInformation   {grid-position  (align = center), image-file-position, scale, rotate}
	name               str
	'''
	def __init__(self, order, adhesionFrame, imageInformation, name, startBlockInfo):
		super(obj_player, self).__init__()
		self.name = name
		self.money = 5000                     # Change initial value here
		self.status = dict()
		self.steps = 0
		self.position = 0
		self.order = order
		self.adhesionFrame = adhesionFrame
		self.grid_positions = imageInformation["grid-position"]
		self.animationBuffer = 0
		self.estate = list()
		self.bankrupted = False
		self.startBlock = startBlockInfo
		# Read Image
		self.image = pygame.image.load(imageInformation["image-file-position"])
		self.image = pygame.transform.scale(self.image, imageInformation["scale"])
		self.image = pygame.transform.rotate(self.image, imageInformation["rotate"])
		self.img_position = self.grid_positions[0]
		self.img_margin = ([self.image.get_width(), 0, self.image.get_width(), 0][self.order], [self.image.get_height(), self.image.get_height(), 0, 0][self.order])
		self.img_position = (self.img_position[0] + self.img_margin[0], self.img_position[1] + self.img_margin[1])
		# Command
		self.showOnScreen = lambda:self.adhesionFrame.blit(self.image, self.img_position)
	def __gt__(self, other):
		self.steps = other
	def statusReduction(self):
		for sta in dict(self.status):
			self.status[sta] -= 1
			if self.status[sta] <= 0:del self.status[sta]
	def positionUpdate(self):
		if self.steps > 0 and self.animationBuffer <= 0:
			self.position += 1
			if self.position >= len(self.grid_positions):
				self.position %= len(self.grid_positions)
				exec(self.startBlock.command.replace("target", "self"))
			self.img_position = self.grid_positions[self.position]
			self.img_position = (self.img_position[0] + self.img_margin[0], self.img_position[1] + self.img_margin[1])
			self.steps -= 1
			self.animationBuffer = 20
		elif self.steps == 0:return True
		else:self.animationBuffer -= 1
class obj_dice(object):
	def __init__(self, adhesionFrame):
		super(obj_dice, self).__init__()
		self.w, self.h = pygame.display.get_surface().get_size()
		self.adhesionFrame = adhesionFrame
		self.font = pygame.font.SysFont("comicsans", 100)
		self.k = 6
		self.word = self.font.render(f"{self.k}", 1, (255, 255, 255))
		self.position = (self.w // 2 - self.word.get_width() // 2, self.h // 2 - self.word.get_height() // 2)
		self.showOnScreen = lambda:self.adhesionFrame.blit(self.word, self.position)
		self.getNow = lambda:self.k
	def change(self):
		self.k = random.randint(1, 12)
		self.word = self.font.render(f"{self.k}", 1, (255, 255, 255))
		self.position = (self.w // 2 - self.word.get_width() // 2, self.h // 2 - self.word.get_height() // 2)
class obj_queryBlock(object):
	def __init__(self, adhesionFrame):
		super(obj_queryBlock, self).__init__()
		self.adhesionFrame = adhesionFrame
		self.w, self.h = pygame.display.get_surface().get_size()
		self.image = pygame.image.load(os.path.join("Assets", "purchaseBlock.png"))
		self.img_position = (self.w // 2 - self.image.get_width() // 2, self.h // 2 - self.image.get_height() // 2)
		self.yes = pygame.Rect(self.w // 2 - 50, self.h // 2 + 20, 0, 0).inflate(70, 30) 
		self.no = pygame.Rect(self.w // 2 + 50, self.h // 2 + 20, 0, 0).inflate(70, 30)
		# Command
		self.showOnScreen = lambda:self.adhesionFrame.blit(self.image, self.img_position)
	def getResult(self):
		point = pygame.mouse.get_pos()
		self.collide_yes = self.yes.collidepoint(point)
		self.collide_no = self.no.collidepoint(point)
		return bool(self.collide_yes | self.collide_no)
class gam_roundHandler(object):
	def __init__(self, playerNames):
		super(gam_roundHandler, self).__init__()
		self.ply_names = playerNames
		self.process = ["getRandom", "move", "calculate"]
		self.round = 1
		# Command
		self.whoIsOn = lambda:(self.round - 1, self.ply_names[self.round - 1])
	def __next__(self):
		self.round = (self.round + 1) if self.round < len(self.ply_names) else (1)
class Game(object):
	def __init__(self, playerNames):
		super(Game, self).__init__()
		screenArguments = {"size" : (940, 940), "align" : "left", "margin" : 40}
		nowMap = mod_mapFileReader("classic.mon")
		countGrid = mod_coordinateCalculator(screenArguments, {
			"size" : nowMap.blk_size, "amount" : nowMap.blk_amount
		})
		self.playerNames = playerNames
		self.window = pygame.display.set_mode(screenArguments["size"])
		self.FPS = 60
		self.blocks = [obj_block(self.window, (i, obj[0][0]), {"grid-position" : obj[0][1], "scale" : countGrid.getScale(), "rotate" : obj[1]})for i, obj in enumerate(zip(zip(nowMap.getBlocksInformation().values(), countGrid.getPositions(align = 0)), countGrid.getRotaters()))]
		self.players = [obj_player(i, self.window, {"grid-position" : countGrid.getPositions(align = 1), "image-file-position" : os.path.join("Assets", f"{obj}.png"), "scale" : (20, 20), "rotate" : 0}, obj, self.blocks[0])for i, obj in enumerate(playerNames)]
		self.clock = pygame.time.Clock()
		self.animationLock = False
		self.round = gam_roundHandler(playerNames)
		self.dice = obj_dice(self.window)
		self.queryBlock = obj_queryBlock(self.window)
		self.renderQuery = False
		self.click = False
		self.waiting = False
		self.moneyWords = []
		# Command
		self.isAffordable = lambda players, price:players.money >= price
	def update(self):
		nowPlayer = self.players[self.round.whoIsOn()[0]]
		if not self.animationLock:
			if nowPlayer.bankrupted: 
				next(self.round)
			elif "inJail" in nowPlayer.status.keys():
				nowPlayer.statusReduction()
				next(self.round)
			elif "Mortocycle" in nowPlayer.status:
				nowPlayer > random.randint(0, len(self.blocks))
				self.animationLock = True
			else:self.dice.change()
		else:
			rst = nowPlayer.positionUpdate()
			if rst == True:
				self.waiting = True
		if self.waiting == True:self.executeMovement(nowPlayer, self.blocks[nowPlayer.position])
		self.eventControl()
		self.render()
		self.clock.tick(self.FPS)
	def eventControl(self):
		for event in pygame.event.get():
			self.click = event.type == pygame.MOUSEBUTTONUP
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				
				if not self.animationLock:
					if event.key == pygame.K_SPACE:
						self.animationLock = True
						self.players[self.round.whoIsOn()[0]] > self.dice.getNow()
	def render(self):
		self.window.fill((0, 0, 0))
		self.dice.showOnScreen()
		for i, ply in enumerate(self.players):
			w, h = pygame.display.get_surface().get_size()
			font = pygame.font.SysFont("comicsans", 40)
			word = font.render(f"{ply.name}:${ply.money}", 1, (255, 255, 255))
			position = [(10, 10), (10, w - word.get_height()), (h - word.get_width(), 10), (w - word.get_width(), h - word.get_height())][i]
			self.window.blit(word, position)
		for obj in self.blocks:obj.showOnScreen()
		for obj in self.players:obj.showOnScreen()
		if self.renderQuery:self.queryBlock.showOnScreen()
		pygame.display.update()
	def executeMovement(self, nowPlayer, nowBlock):
		if nowBlock.category == "special":
			nowPlayer.statusReduction()
			exec(nowBlock.command.replace("target", "nowPlayer"))
			self.animationLock = False
			self.waiting = False
			next(self.round)
		else:
			if nowBlock.propiertary != '' and nowBlock.propiertary != nowPlayer.name:
				while not self.isAffordable(nowPlayer, nowBlock.tolls[nowBlock.houses]):
					if len(nowPlayer.estate) != 0:
						random.shuffle(nowPlayer.estate)
						soldBlock = self.blocks[nowPlayer.estate[0]]
						nowPlayer.money += soldBlock.sellPrice[soldBlock.houses]
						soldBlock.houses = 0
						soldBlock.propiertary = ""
					else:
						nowPlayer.bankrupted = True
						break
				nowPlayer.money -= nowBlock.tolls[nowBlock.houses]
				self.players[self.playerNames.index(nowBlock.propiertary)].money += nowBlock.tolls[nowBlock.houses]
				self.animationLock = False
				self.waiting = False
				nowPlayer.statusReduction()
				next(self.round)
				return True
			if self.queryBlock.getResult() and self.click:
				self.renderQuery = False
				if self.queryBlock.collide_yes:
					if nowBlock.propiertary == "":
						if self.isAffordable(nowPlayer, nowBlock.purchasePrice[0]):
							nowPlayer.money -= nowBlock.purchasePrice[0]
							nowBlock.propiertary = nowPlayer.name
							nowPlayer.estate.append(nowBlock.index)
					elif nowBlock.propiertary == nowPlayer.name and nowBlock.houses < len(nowBlock.purchasePrice):
						if self.isAffordable(nowPlayer, nowBlock.purchasePrice[nowBlock.houses + 1]):
							nowPlayer.money -= nowBlock.purchasePrice[nowBlock.houses + 1]
							nowBlock.houses += 1
				self.animationLock = False
				self.waiting = False
				nowPlayer.statusReduction()
				next(self.round)
				return True
			else:
				self.renderQuery = True


game = Game(["alpha", "mighty", "fox", "frot"])
while True:
	game.update()

