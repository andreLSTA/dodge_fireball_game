import pygame
import os
import time
import random
import math
import numpy as np

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Dodge Fireball Game")

# Load images
BLUE_FIREBALL = []
for i in range(6):
	BLUE_FIREBALL.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue_fireball_"+str(i+1)+".png")), (100, 40)) )

PLAYER = []
for i in range(10):
	PLAYER.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "char_walking_"+str(i+1)+".png")), (70, 100)) )


BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "forest_background.png")), (WIDTH, HEIGHT))

class Fireball():
	def __init__(self, x, y, angle):
		self.fireball_img = BLUE_FIREBALL[0]
		self.rect = self.fireball_img.get_rect()
		self.rect.center = (x, y)
		self.mask = pygame.mask.from_surface(self.fireball_img)
		self.angle = angle
		self.frame = 0
		self.speed = 10
		self.not_in_the_screen = False

	def draw(self, window):
		self.frame = (self.frame + 1) % (4*len(BLUE_FIREBALL))
		self.fireball_img = pygame.transform.rotate(BLUE_FIREBALL[int(self.frame/4 - 1)], self.angle)
		self.mask = pygame.mask.from_surface(self.fireball_img)
		x, y = self.rect.center
		self.rect = self.fireball_img.get_rect()
		self.rect.center = (x, y)
		window.blit(self.fireball_img, self.rect)

	def rotateLeft(self):
		self.angle = (self.angle - 5) % 360

	def rotateRight(self):
		self.angle = (self.angle + 5) % 360

	def move(self):
		current_x, current_y = self.rect.center
		angle = math.radians(self.angle)
		x = -self.speed*math.cos(angle)

		if(current_x + x >= -150 and current_x + x <= WIDTH + 150):
			current_x += x
		else:
			self.not_in_the_screen = True

		y = self.speed*math.sin(angle)
		if(current_y + y >= -150 and current_y + y <= HEIGHT + 150):
			current_y += y
		else:
			self.not_in_the_screen = True

		self.rect = self.fireball_img.get_rect()
		self.rect.center = (current_x, current_y)


class Player():
	def __init__(self, x, y):
		self.player_img = PLAYER[0]
		self.rect = self.player_img.get_rect()
		self.rect.center = (x, y)
		self.mask = pygame.mask.from_surface(self.player_img)
		self.frame = 0
		self.speed = 5
		self.angle = 0
		self.flip = False

	def draw(self, window):
		self.frame = (self.frame + 1) % (2.5*len(PLAYER))
		self.player_img = pygame.transform.flip(PLAYER[int(self.frame/2.5 - 1)], self.flip, False)
		self.mask = pygame.mask.from_surface(self.player_img)
		x, y = self.rect.center
		self.rect = self.player_img.get_rect()
		self.rect.center = (x, y)
		window.blit(self.player_img, self.rect)

	def moveLeft(self):
		current_x, current_y = self.rect.center
		if(current_x - self.speed >= 0):
			current_x -= self.speed

		self.flip = True
		self.updateCenter(current_x, current_y)

	def moveRight(self):
		current_x, current_y = self.rect.center
		if(current_x + self.speed <= WIDTH):
			current_x += self.speed

		self.flip = False
		self.updateCenter(current_x, current_y)

	def moveUp(self):
		current_x, current_y = self.rect.center
		if(current_y - self.speed >= HEIGHT*0.34):
			current_y -= self.speed

		self.updateCenter(current_x, current_y)

	def moveDown(self):
		current_x, current_y = self.rect.center
		if(current_y + self.speed <= HEIGHT):
			current_y += self.speed

		self.updateCenter(current_x, current_y)

	def updateCenter(self, current_x, current_y):
		self.rect = self.player_img.get_rect()
		self.rect.center = (current_x, current_y)

	def collidedWith(self, obj):
		return pygame.sprite.spritecollide(self, [obj], False, pygame.sprite.collide_mask)


def generateFireball(player_position_x, player_position_y):
	
	choice = random.randint(1, 4)
	fireball_position_x = 0
	fireball_position_y = 0
	fireball_angle = 0
	if(choice == 1):
		fireball_position_x = -150
		fireball_position_y = random.randint(-150, HEIGHT + 150)
	elif(choice == 2):
		fireball_position_x = WIDTH + 150
		fireball_position_y = random.randint(-150, HEIGHT + 150)
	elif(choice == 3):
		fireball_position_x = random.randint(-150, WIDTH + 150)
		fireball_position_y = -150
	else:
		fireball_position_x = random.randint(-150, WIDTH + 150)
		fireball_position_y = HEIGHT + 150

	fireball_angle = (math.degrees(math.atan2((fireball_position_y - player_position_y), (player_position_x - fireball_position_x))) + 180) % 360
	return Fireball(fireball_position_x, fireball_position_y, fireball_angle)


def runGame(FPS, clock):
	run = True
	fireballs_survived = 0
	quantity_fireballs = 5
	wave = 1
	player = Player(WIDTH/2, HEIGHT/2)
	fireballs = []
	
	def updateGameWindow():
		WIN.blit(BACKGROUND, (0,0))
		player.draw(WIN)
		for fireball in fireballs:
			fireball.draw(WIN)

		pygame.font.init()
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("Wave: " + str(wave), 1, (255,255,255))
		WIN.blit(label, (WIDTH - 100, 15))
				
		pygame.display.update()	

	while(run):
		clock.tick(FPS)
		updateGameWindow()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		if(len(fireballs) == 0):

			quantity_fireballs += 1
			wave += 1
			fireballs_survived = 0

			while len(fireballs) < quantity_fireballs:
				fireballs.append(generateFireball(player.rect.center[0], player.rect.center[1]))

		
		keys = pygame.key.get_pressed()
		if(keys[pygame.K_a]):
			player.moveLeft()
		if(keys[pygame.K_d]):
			player.moveRight()
		if(keys[pygame.K_w]):
			player.moveUp()
		if(keys[pygame.K_s]):
			player.moveDown()

		to_remove = []

		for fireball_index, fireball in enumerate(fireballs):
			
			if(player.collidedWith(fireballs[fireball_index])):
				run = False
				break

			fireballs[fireball_index].move()
			
			if(fireballs[fireball_index].not_in_the_screen):
				to_remove.append(fireball_index)

		for fireball_index in reversed(to_remove):
			del fireballs[fireball_index]

def gameOverScreen(FPS, clock):
	run = True
	while(run):
		clock.tick(FPS)
		myfont = pygame.font.SysFont("monospace", 50)
		label = myfont.render("Game Over", 1, (255,255,255))
		myfont_2 = pygame.font.SysFont("monospace", 25)
		label_2 = myfont_2.render("(press R to restart)", 1, (255,255,255))
		
		WIN.blit(label, (WIDTH*0.37, HEIGHT*0.5))
		WIN.blit(label_2, (WIDTH*0.36, HEIGHT*0.6))
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		keys = pygame.key.get_pressed()
		if(keys[pygame.K_r]):
			break	

	return run


def main():
	FPS = 60
	clock = pygame.time.Clock()
	run = True
	while(run):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		
		runGame(FPS, clock)	
		run = gameOverScreen(FPS, clock)			
				
main()