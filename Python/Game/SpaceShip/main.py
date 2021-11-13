import pygame
import os
pygame.font.init()
pygame.mixer.init()

width, height = 900, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Go! Escape")
FPS = 60
velocity = 5
bullet_velocity = 6
spaceship_width, spaceship_height = 55, 40

yellow_hit = pygame.USEREVENT + 1
red_hit = pygame.USEREVENT + 2

border = pygame.Rect(width//2 - 5, 0, 10, height)
bullet_hit_sound = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
bullet_fire_sound = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

health_font = pygame.font.SysFont("comicsans", 40)
winner_font = pygame.font.SysFont("comicsans", 100)

max_bullet = 3

space = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (width, height))

yellow_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
yellow_spaceship_image = pygame.transform.scale(yellow_spaceship_image, (spaceship_width, spaceship_height))
yellow_spaceship_image = pygame.transform.rotate(yellow_spaceship_image, 90)

red_spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
red_spaceship_image = pygame.transform.scale(red_spaceship_image, (spaceship_width, spaceship_height))
red_spaceship_image = pygame.transform.rotate(red_spaceship_image, -90)


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
	for bullet in yellow_bullets:
		bullet.x += bullet_velocity
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(red_hit))
			yellow_bullets.remove(bullet)
		elif bullet.x > width:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= bullet_velocity
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(yellow_hit))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)

def draw_winner(text):
	draw_text = winner_font.render(text, 1, (255, 255, 255))
	win.blit(draw_text, (width/2 - draw_text.get_width(), height/2 - draw_text.get_height()))
	pygame.display.update()
	pygame.time.delay(5000)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
	win.blit(space, (0, 0))
	pygame.draw.rect(win, (0, 0, 0), border)

	red_health_text = health_font.render(f'Health:{red_health}', 1, (255, 255, 255))
	yellow_health_text = health_font.render(f'Health:{yellow_health}', 1, (255, 255, 255))
	win.blit(red_health_text, (width - red_health_text.get_width() - 10, 10))
	win.blit(yellow_health_text, (10, 10))

	win.blit(yellow_spaceship_image, (yellow.x, yellow.y))
	win.blit(red_spaceship_image, (red.x, red.y))

	for bullet in red_bullets:
		pygame.draw.rect(win, (255, 0, 0), bullet)
	for bullet in yellow_bullets:
		pygame.draw.rect(win, (255, 255, 0), bullet)

	pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
	if keys_pressed[pygame.K_a] and yellow.x - velocity > 0: # Left
		yellow.x -= velocity
	if keys_pressed[pygame.K_d] and yellow.x + velocity < border.x - spaceship_height: # Left
		yellow.x += velocity
	if keys_pressed[pygame.K_w] and yellow.y - velocity > 0: # Left
		yellow.y -= velocity
	if keys_pressed[pygame.K_s] and yellow.y + velocity < height - spaceship_width: # Left
		yellow.y += velocity

def red_handle_movement(keys_pressed, red):
	if keys_pressed[pygame.K_LEFT] and red.x - velocity > border.x: # Left
		red.x -= velocity
	if keys_pressed[pygame.K_RIGHT] and red.x + velocity < 900 - spaceship_height: # Left
		red.x += velocity
	if keys_pressed[pygame.K_UP] and red.y - velocity > 0: # Left
		red.y -= velocity
	if keys_pressed[pygame.K_DOWN] and red.y + velocity < height - spaceship_width: # Left
		red.y += velocity


def main():
	yellow = pygame.Rect(100, 300, spaceship_width, spaceship_height)
	red = pygame.Rect(700, 300, spaceship_width, spaceship_height)

	red_bullets = []
	yellow_bullets = []

	yellow_health = 10
	red_health = 10

	clock = pygame.time.Clock()
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullet:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 4)
					yellow_bullets.append(bullet)
					bullet_fire_sound.play()
				if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullet:
					bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 4)
					red_bullets.append(bullet)
					bullet_fire_sound.play()
			if event.type == red_hit:
				red_health -= 1
				bullet_hit_sound.play()
			if event.type == yellow_hit:
				yellow_health -= 1
				bullet_hit_sound.play()
		winner_text = ""
		if red_health <= 0:
			winner_text = "Yellow wins!"
		if yellow_health <= 0:
			winner_text = "Red wins!"
		if winner_text != "":
			draw_winner(winner_text)
			break

		keys_pressed = pygame.key.get_pressed()
		yellow_handle_movement(keys_pressed, yellow)
		red_handle_movement(keys_pressed, red)

		handle_bullets(yellow_bullets, red_bullets, yellow, red)

		draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
		clock.tick(FPS)

	main()

if __name__ == "__main__":
	main()