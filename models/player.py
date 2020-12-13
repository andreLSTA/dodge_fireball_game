import pygame
import os
import math
from models.screen_size import WIDTH, HEIGHT

# Load images
WATER_CHAR = []
for i in range(10):
	WATER_CHAR.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "water_char_running_"+str(i+1)+".png")), (75, 100)) )

FIRE_CHAR = []
for i in range(10):
	FIRE_CHAR.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "fire_char_running_"+str(i+1)+".png")), (75, 100)) )

colors = {
	"red": FIRE_CHAR,
	"blue": WATER_CHAR 
}

class Player():
	def __init__(self, x, y, color):
		self.player_img = colors[color][0]
		self.rect = self.player_img.get_rect()
		self.rect.center = (x, y)
		self.mask = pygame.mask.from_surface(self.player_img)
		self.color = color
		self.frame = 0
		self.speed = 5
		self.angle = 0
		self.flip = False
		

	def draw(self, window):
		self.frame = (self.frame + 1) % (2.5*len(colors[self.color]))
		self.player_img = pygame.transform.flip(colors[self.color][int(self.frame/2.5 - 1)], self.flip, False)		
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
		if(current_y - self.speed >= HEIGHT*0.35):
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