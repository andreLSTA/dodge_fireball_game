import pygame
import os
import math
from models.screen_size import WIDTH, HEIGHT

# Load images
BLUE_FIREBALL = []
for i in range(6):
	BLUE_FIREBALL.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "blue_fireball_"+str(i+1)+".png")), (100, 40)) )

RED_FIREBALL = []
for i in range(6):
	RED_FIREBALL.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "red_fireball_"+str(i+1)+".png")), (100, 40)) )

colors = {
	"red": RED_FIREBALL,
	"blue": BLUE_FIREBALL
}

class Fireball():
	def __init__(self, x, y, angle, color):
		self.fireball_img = colors[color][0]
		self.rect = self.fireball_img.get_rect()
		self.rect.center = (x, y)
		self.mask = pygame.mask.from_surface(self.fireball_img)
		self.angle = angle
		self.color= color
		self.frame = 0
		self.speed = 10
		self.not_in_the_screen = False		

	def draw(self, window):
		self.frame = (self.frame + 1) % (4*len(colors[self.color]))
		self.fireball_img = pygame.transform.rotate(colors[self.color][int(self.frame/4 - 1)], self.angle)
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
