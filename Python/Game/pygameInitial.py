import pygame
import sys
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

width, height = 900, 500

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("GameName")

FPS = 60

while True:
	clock = pygame.time.Clock()
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	clock.tick(FPS)