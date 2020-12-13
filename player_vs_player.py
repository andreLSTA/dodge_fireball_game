import pygame
import os
import time
import random
import math
import numpy as np
import pickle
from models.fireball import Fireball
from models.player import Player
from models.neural_network import NeuralNetwork

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
GAME_HEIGHT = HEIGHT - 0.35*HEIGHT
pygame.display.set_caption("Dodge Fireball Game")

# Load images
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "forest_background.png")), (WIDTH, HEIGHT))

def createFireballs(player_position_x, player_position_y, color):
	
	left_fireball = Fireball(-150, player_position_y*(np.random.rand()*0.3 + 0.85), 180, color)
	right_fireball = Fireball(WIDTH+150, player_position_y*(np.random.rand()*0.3 + 0.85), 0, color)
	top_fireball = Fireball(player_position_x*(np.random.rand()*0.3 + 0.85), -150, 90, color)
	bottom_fireball = Fireball(player_position_x*(np.random.rand()*0.3 + 0.85), HEIGHT+150, 270, color)

	speeds = [12, 15, 18, 21]
	left_fireball.speed = np.random.choice(speeds)
	right_fireball.speed = np.random.choice(speeds)
	top_fireball.speed = np.random.choice(speeds)
	bottom_fireball.speed = np.random.choice(speeds)

	return [left_fireball, right_fireball, top_fireball, bottom_fireball]

def buildNeuralNetworkInputs(bot, bot_fireballs):
		
	player_position_x, player_position_y = bot.rect.center
	
	dL = player_position_x/WIDTH
	dR = 1 - dL
	dT = (player_position_y - HEIGHT*0.34)/(HEIGHT - HEIGHT*0.34)
	dB = 1 - dT

	inputs = []

	inputs.append(dL)
	inputs.append(dR)
	inputs.append(dT)
	inputs.append(dB)

	for fireball_index, fireball in enumerate(bot_fireballs):
		
		fireball_position_x, fireball_position_y = fireball.rect.center
		distance_to_fireball_x = (player_position_x - fireball_position_x)/(WIDTH)
		distance_to_fireball_y = (player_position_y - fireball_position_y)/(HEIGHT)
		distance = (distance_to_fireball_x**2 + distance_to_fireball_y**2)**(1/2)	
		fireball_speed = (fireball.speed-10)/10.0

		inputs.append(distance)
		inputs.append(distance_to_fireball_x)
		inputs.append(distance_to_fireball_y)
		inputs.append(fireball_speed)

	return inputs

def moveFireballs(fireballs):

	for fireball_index, fireball in enumerate(fireballs):
		fireball.move()

def checkCollision(player, fireballs):

	for fireball_index, fireball in enumerate(fireballs):
		if(player.collidedWith(fireball)):
			return True

	return False

def countFireballsOnScreen(fireballs):

	fireballs_on_screen = 4

	for fireball_index, fireball in enumerate(fireballs):
		if(fireball.not_in_the_screen):
			fireballs_on_screen -= 1

	return fireballs_on_screen


def runGame(FPS, clock):
	run = True
	timer = 0
	fire_player_fireballs_on_screen = 4
	water_player_fireballs_on_screen = 4
	fire_player = Player(WIDTH/2, HEIGHT/2, "red")
	water_player = Player(WIDTH/2, HEIGHT/2, "blue")
	fire_player_fireballs = createFireballs(fire_player.rect.center[0], fire_player.rect.center[1], "blue")
	water_player_fireballs = createFireballs(water_player.rect.center[0], water_player.rect.center[1], "red")

	def updateGameWindow():
		WIN.blit(BACKGROUND, (0,0))
		
		fire_player.draw(WIN)
		water_player.draw(WIN)

		for fire_player_fireball in fire_player_fireballs:
			fire_player_fireball.draw(WIN)

		for water_player_fireball in water_player_fireballs:
			water_player_fireball.draw(WIN)

		pygame.font.init()
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("Timer: " + str(round(timer, 2)), 1, (255,255,255))
		WIN.blit(label, (WIDTH - 125, 15))
				
		pygame.display.update()	

	while(run):
		clock.tick(FPS)
		updateGameWindow()

		timer += 1/FPS

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		if(fire_player_fireballs_on_screen == 0):
			fire_player_fireballs = createFireballs(fire_player.rect.center[0], fire_player.rect.center[1], "blue")

		if(water_player_fireballs_on_screen == 0):
			water_player_fireballs = createFireballs(water_player.rect.center[0], water_player.rect.center[1], "red")

		
		keys = pygame.key.get_pressed()	

		# FIRE PLAYER CONTROLLER		
		if(keys[pygame.K_a]):
			fire_player.moveLeft()
		if(keys[pygame.K_d]):
			fire_player.moveRight()
		if(keys[pygame.K_w]):
			fire_player.moveUp()
		if(keys[pygame.K_s]):
			fire_player.moveDown()

		# WATER PLAYER CONTROLLER
		if(keys[pygame.K_LEFT]):
			water_player.moveLeft()					
		if(keys[pygame.K_RIGHT]):
			water_player.moveRight()
		if(keys[pygame.K_UP]):
			water_player.moveUp()
		if(keys[pygame.K_DOWN]):
			water_player.moveDown()

		moveFireballs(fire_player_fireballs)
		moveFireballs(water_player_fireballs)

		if(checkCollision(fire_player, fire_player_fireballs)):
			return "Water"
		
		if(checkCollision(water_player, water_player_fireballs)):
			return "Fire"

		fire_player_fireballs_on_screen = countFireballsOnScreen(fire_player_fireballs)
		water_player_fireballs_on_screen = countFireballsOnScreen(water_player_fireballs)


def gameOverScreen(FPS, clock, winner):
	run = True
	while(run):
		clock.tick(FPS)
		myfont = pygame.font.SysFont("monospace", 50)
		label = myfont.render(winner + " won!", 1, (255,255,255))
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
		
		winner = runGame(FPS, clock)	
		run = gameOverScreen(FPS, clock, winner)			
				
main()