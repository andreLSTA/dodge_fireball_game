import pygame
import os
import time
import math
import numpy as np
import pickle
from models.fireball import Fireball
from models.player import Player
from models.neural_network import NeuralNetwork
from models.screen_size import WIDTH, HEIGHT

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
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

def buildNeuralNetworkInputs(player, player_fireballs):
		
	player_position_x, player_position_y = player.rect.center
	
	dL = player_position_x/WIDTH
	dR = 1 - dL
	dT = (player_position_y - HEIGHT*0.35)/(HEIGHT - HEIGHT*0.35)
	dB = 1 - dT

	inputs = []

	inputs.append(dL)
	inputs.append(dR)
	inputs.append(dT)
	inputs.append(dB)

	for fireball_index, fireball in enumerate(player_fireballs):
		
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
	population = 1000
	highest_wave = 0
	generation_stagnation=0
	best_highest_wave = 0
	average_wave = 0
	generation = 0
	mutation_rate = 0.05
	mutation_percentage = 1.0
	wave = [0 for i in range(population)]
	players = [Player(WIDTH/2, HEIGHT/2, "red") for i in range(population)]
	fireballs = [createFireballs(players[i].rect.center[0], players[i].rect.center[1], "blue") for i in range(population)]
	fireballs_on_screen = [4 for i in range(population)]
	neural_networks = [NeuralNetwork(20, 12, 4) for i in range(population)]
	
	best_neural_networks = []

	def updateGameWindow():
		WIN.blit(BACKGROUND, (0,0))

		i = 0
		for player in players:
			if(i < 1):
				player.draw(WIN)
				
				for fireball in fireballs[i]:
					fireball.draw(WIN)

				i += 1	

		pygame.font.init()
		myfont = pygame.font.SysFont("monospace", 15)
		label = myfont.render("Wave: " + str(highest_wave), 1, (255,255,255))
		WIN.blit(label, (WIDTH - 220, 15))
				
		pygame.display.update()	

	while(run):
		
		clock.tick(FPS)
		updateGameWindow()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# GENERATE NEW PLAYERS IF THEY'RE ALL DEAD
		if(len(players) == 0):

			generation += 1 

			if(highest_wave > best_highest_wave):
				generation_stagnation = 0
				best_highest_wave = highest_wave
			else:
				generation_stagnation += 1

			print("------ GENERATION ", generation, "------")
			print("Average wave:", average_wave)
			print("Highest wave:", highest_wave)
			print("Best highest wave:", best_highest_wave)
			print("Generation stagnation:", generation_stagnation)
			print("-----------------------------")

			pickle.dump( best_neural_networks[-1], open( "neural_network.p", "wb" ) )

			if(average_wave >= 100):
				break

			if(generation_stagnation >= 10):
				mutation_percentage = mutation_percentage*0.8
				generation_stagnation = 0
			
			highest_wave = 0
			average_wave = 0
			wave = [0 for i in range(population)]			
			players = [Player(WIDTH/2, HEIGHT/2, "red") for i in range(population)]
			fireballs = [createFireballs(players[i].rect.center[0], players[i].rect.center[1], "blue") for i in range(population)]	
			fireballs_on_screen = [4 for i in range(population)]
			neural_networks = [NeuralNetwork(20, 12, 4) for i in range(population)]
			
			for i in range(len(neural_networks)):
				neural_networks[i].crossover(np.random.choice(best_neural_networks, 1))
				neural_networks[i].mutation(mutation_rate, mutation_percentage)
			
			best_neural_networks = []

		# GENERATE FIREBALLS
		for i in range(len(fireballs)):
			if(fireballs_on_screen[i] == 0):
				wave[i] += 1
				
				if(wave[i] > highest_wave):
					highest_wave = wave[i]

				fireballs[i] = createFireballs(players[i].rect.center[0], players[i].rect.center[1], "blue")

		
		# PLAYER MOVEMENT
		for player_index, player in enumerate(players):
			
			inputs = buildNeuralNetworkInputs(player, fireballs[player_index])		
			outputs = neural_networks[player_index].predict(inputs)
			if(outputs[0]):
				players[player_index].moveUp()					
			if(outputs[1]):
				players[player_index].moveDown()
			if(outputs[2]):
				players[player_index].moveLeft()
			if(outputs[3]):
				players[player_index].moveRight()

		# CHECK PLAYER COLLISION
		to_remove = []
		for player_index, player in enumerate(players):
			if(checkCollision(player, fireballs[player_index])):
				highest_wave = wave[player_index]	
				to_remove.append(player_index)

		# REMOVE COLLIDED PLAYERS
		for index in reversed(to_remove):

			if(len(players) <= 0.02*population):
				best_neural_networks.append(neural_networks[index])
				average_wave += wave[index]/(0.02*population)

			del players[index]
			del neural_networks[index]
			del fireballs[index]
			del fireballs_on_screen[index]
			del wave[index]

		# MOVE FIREBALL
		for i in range(len(fireballs)):
			moveFireballs(fireballs[i])
			fireballs_on_screen[i] = countFireballsOnScreen(fireballs[i])




def gameOverScreen(FPS, clock):
	run = True
	while(run):
		clock.tick(FPS)
		myfont = pygame.font.SysFont("monospace", 50)
		label = myfont.render("Game Over", 1, (255,255,255))
		WIN.blit(label, (WIDTH*0.37, HEIGHT*0.5))
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

def main():
	FPS = 60
	clock = pygame.time.Clock()
	runGame(FPS, clock)	
	gameOverScreen(FPS, clock)			
				
main()