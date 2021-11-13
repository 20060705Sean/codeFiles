import pygame
import os
pygame.init()

const = {
	"window-size" : (500, 800), 
	"window-caption" : "Go 3scape!", 
	"game-fps" : 60,
	"color-black" : (0, 0, 0), 
	"color-white" : (255, 255, 255)
}

window = pygame.display.set_mode(const["window-size"])
pygame.display.set_caption(const["window-caption"])
clock = pygame.time.Clock()

images = {
	"ball-image" : pygame.transform.scale(pygame.image.load(os.path.join("Assets", "black-circle.png")), (30, 30)).convert_alpha(), 
	"ring-part-image" : pygame.transform.scale(pygame.image.load(os.path.join("Assets", "ring-part.png")), (80, 60)).convert_alpha(), 
	"brick-image" : pygame.transform.scale(pygame.image.load(os.path.join("Assets", "brick.png")), (64, 36)).convert_alpha()
}

for i in images.keys():
	images[i].set_colorkey((255,255,255))

masks = {
	pygame.mask.from_surface(images["ball-image"])
}

stableObj = {
	"ring-part" : pygame.Rect(180, 600, 65, 45), 
	"ball" : pygame.Rect(200, 300, 30, 30)
}

movingObj = {
	"brick" : {"object" : pygame.Rect(100, 400, 64, 36),
		"typ" : "move", 
		"status" : "go", # The oppose one is "back" 
		"position" : ((100, 400), (300, 500)),
		"velocity" : (2, 1)
	}
}

ballPhysicData = {
	"ball-in-air" : True, 
	"acceleration" : 14,  
	"velocity": 0
}



def keysController():
	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_SPACE] and not ballPhysicData["ball-in-air"]:
		ballPhysicData["velocity"] = -60
		ballPhysicData["ball-in-air"] = True

def ballPositionChange():
	if ballPhysicData["ball-in-air"]:
		ballPhysicData["velocity"] += ballPhysicData["acceleration"] * (6 / const["game-fps"])
		stableObj["ball"].y += ballPhysicData["velocity"] * (6 / const["game-fps"])
	flag = False
	for obstacle in ["ring-part"]:flag |= stableObj["ball"].colliderect(stableObj[obstacle])
	for obstacle in ["brick"]:flag |= stableObj["ball"].colliderect(movingObj[obstacle]["object"])
	if flag:ballPhysicData["velocity"] = 0
	ballPhysicData["ball-in-air"] = not flag

def movingObjPositionChange():
	for obj in movingObj:
		if movingObj[obj]["typ"] == "move":
			movingObj[obj]["object"].x += movingObj[obj]["velocity"][0] * (1 if movingObj[obj]["status"] == "go" else -1)
			movingObj[obj]["object"].y += movingObj[obj]["velocity"][1] * (1 if movingObj[obj]["status"] == "go" else -1)
			if movingObj[obj]["object"].colliderect(stableObj["ball"]):
				stableObj["ball"].x += movingObj[obj]["velocity"][0] * (1 if movingObj[obj]["status"] == "go" else -1)
				stableObj["ball"].y += movingObj[obj]["velocity"][1] * (1 if movingObj[obj]["status"] == "go" else -1)
			if movingObj[obj]["object"].x == movingObj[obj]["position"][1][0] and movingObj[obj]["object"].y == movingObj[obj]["position"][1][1]:
				movingObj[obj]["status"] = "back"
			elif movingObj[obj]["object"].x == movingObj[obj]["position"][0][0] and movingObj[obj]["object"].y == movingObj[obj]["position"][0][1]:
				movingObj[obj]["status"] = "go"

def render():
	window.fill(const["color-white"])
	for obj in stableObj.keys():window.blit(images[f"{obj}-image"], (stableObj[obj].x, stableObj[obj].y))
	for obj in movingObj.keys():window.blit(images[f"{obj}-image"], (movingObj[obj]["object"].x, movingObj[obj]["object"].y))

	pygame.display.update()

def main():
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		keysController()
		ballPositionChange()
		movingObjPositionChange()
		render()
		clock.tick(const["game-fps"])
	pygame.quit()


if __name__ == "__main__":
	main()