import pygame
import os
import time
import math
import numpy as np
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 1000, 600
DIAGONAL = ((WIDTH + 300)**2 + (HEIGHT + 300)**2)**(1/2)
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
		self.inital_position_x = x
		self.inital_position_y = y
		self.rect = self.fireball_img.get_rect()
		self.rect.center = (x, y)
		self.mask = pygame.mask.from_surface(self.fireball_img)
		self.angle = angle
		self.frame = 0
		self.speed = 50
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
		self.speed = 50
		self.angle = 0
		self.flip = False

	def draw(self, window):
		self.frame = (self.frame + 1) % (4*len(PLAYER))
		self.player_img = pygame.transform.flip(PLAYER[int(self.frame/4 - 1)], self.flip, False)
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

	def move(self, mouse_position_x, mouse_position_y):
		current_x, current_y = self.rect.center
		self.angle = math.degrees(math.atan2((current_y - mouse_position_y), (mouse_position_x - current_x))) % 360
		angle = math.radians(self.angle)
		x = self.speed*math.cos(angle)

		if(abs(x) != 5 and abs(x) >= 0.001):
			if(x > 0):
				self.flip = False
			else:
				self.flip = True

		if(current_x + x >= 0 and current_x + x <= WIDTH):
			current_x += x

		y = -self.speed*math.sin(angle)
		if(current_y + y >= HEIGHT*0.34 and current_y + y <= HEIGHT):
			current_y += y

		self.rect = self.player_img.get_rect()
		self.rect.center = (current_x, current_y)

	def collidedWith(self, obj):
		return pygame.sprite.spritecollide(self, [obj], False, pygame.sprite.collide_mask)

	def collidedWithWall(self):
		current_x, current_y = self.rect.center
		return current_x == 0 or current_x == WIDTH or current_y == 0.34*HEIGHT or current_y == HEIGHT

class NeuralNetwork:
	def __init__(self, input_nodes, hidden_1_nodes, hidden_2_nodes, output_nodes):
		self.input_nodes = input_nodes
		self.hidden_1_nodes = hidden_1_nodes
		self.hidden_2_nodes = hidden_2_nodes
		self.output_nodes = output_nodes
		self.bias = 1.0
		self.wih1 =(np.random.randint(2000, size=(self.hidden_1_nodes, self.input_nodes + 1)) - 1000)/1000
		self.wh1h2 = (np.random.randint(2000, size=(self.hidden_2_nodes, self.hidden_1_nodes + 1)) - 1000)/1000
		self.wh2o = (np.random.randint(2000, size=(self.output_nodes, self.hidden_2_nodes + 1)) - 1000)/1000
		

	def sigmoid(self, x):
  		return 1 / (1 + math.exp(-x))

	def inputsScaler(self, inputs, quantity_fireballs):
		scaled_inputs = []
		
		for i in range(quantity_fireballs):
			scaled_inputs.append((inputs[(0+i*quantity_fireballs)%len(inputs)]))
			scaled_inputs.append((inputs[(1+i*quantity_fireballs)%len(inputs)]))
			scaled_inputs.append((inputs[(2+i*quantity_fireballs)%len(inputs)]))
			scaled_inputs.append((inputs[(3+i*quantity_fireballs)%len(inputs)]))
			scaled_inputs.append((inputs[(4+i*quantity_fireballs)%len(inputs)]))
			scaled_inputs.append((inputs[(5+i*quantity_fireballs)%len(inputs)]))


		return scaled_inputs

	def generateWeightsFromParent(self, parent_neural_network, percentage):
		for i in range(len(parent_neural_network.wih1)):
			for j in range(len(parent_neural_network.wih1[i])):
				self.wih1[i][j] = round(parent_neural_network.wih1[i][j] + (np.random.randint(percentage*1000)/1000)*np.random.choice([-1.0, 0, 1.0]), 3)
				if(self.wih1[i][j] > 1):
					self.wih1[i][j] = 1.0
				elif(self.wih1[i][j] < -1):
					self.wih1[i][j] = -1.0

		for i in range(len(parent_neural_network.wh1h2)):
			for j in range(len(parent_neural_network.wh1h2[i])):
				self.wh1h2[i][j] = round(parent_neural_network.wh1h2[i][j] + (np.random.randint(percentage*1000)/1000)*np.random.choice([-1.0, 0, 1.0]), 3)
				if(self.wh1h2[i][j] > 1):
					self.wh1h2[i][j] = 1.0
				elif(self.wh1h2[i][j] < -1):
					self.wh1h2[i][j] = -1.0

		for i in range(len(parent_neural_network.wh2o)):
			for j in range(len(parent_neural_network.wh2o[i])):
				self.wh2o[i][j] = round(parent_neural_network.wh2o[i][j] + (np.random.randint(percentage*1000)/1000)*np.random.choice([-1.0, 0, 1.0]), 3)
				if(self.wh2o[i][j] > 1):
					self.wh2o[i][j] = 1.0
				elif(self.wh2o[i][j] < -1):
					self.wh2o[i][j] = -1.0

	def predict(self, inputs_list, quantity_fireballs):
		inputs_list = self.inputsScaler(inputs_list, quantity_fireballs)
		inputs_list.append(self.bias)
		inputs = np.array(inputs_list, ndmin=2).T
		
		hidden_1_inputs = np.dot(self.wih1, inputs)
		
		hidden_1_outputs = np.maximum(hidden_1_inputs, 0)
		hidden_1_outputs = np.append(hidden_1_outputs, [[self.bias]], axis=0)


		hidden_2_inputs = np.dot(self.wh1h2, hidden_1_outputs)

		hidden_2_outputs = np.maximum(hidden_2_inputs, 0)
		hidden_2_outputs = np.append(hidden_2_outputs, [[self.bias]], axis=0)

		final_inputs = np.dot(self.wh2o, hidden_2_outputs)

		final_outputs = np.maximum(final_inputs, 0)

		inputs_list.pop()
		boolean_output = []
		for final_output in final_outputs:
			if(final_output>0.0):
				boolean_output.append(True)
			else:
				boolean_output.append(False)

		
		return boolean_output

def generateFireball(player_position_x, player_position_y):
	
	choice = np.random.randint(1, 4)
	fireball_position_x = 0
	fireball_position_y = 0
	fireball_angle = 0
	if(choice == 1):
		fireball_position_x = -150
		fireball_position_y = np.random.randint(-150, HEIGHT + 150)
	elif(choice == 2):
		fireball_position_x = WIDTH + 150
		fireball_position_y = np.random.randint(-150, HEIGHT + 150)
	elif(choice == 3):
		fireball_position_x = np.random.randint(-150, WIDTH + 150)
		fireball_position_y = -150
	else:
		fireball_position_x = np.random.randint(-150, WIDTH + 150)
		fireball_position_y = HEIGHT + 150

	fireball_angle = (math.degrees(math.atan2((fireball_position_y - player_position_y), (player_position_x - fireball_position_x))) + 180) % 360
	return Fireball(fireball_position_x, fireball_position_y, fireball_angle)

def generateFireball2(player_position_x, player_position_y):
	
	choice = np.random.randint(1, 5)
	choice2 = np.random.randint(1, 3)
	fireball_position_x = 0
	fireball_position_y = 0
	fireball_angle = 0
	if(choice == 1):
		fireball_position_x = -150
		if(choice2 == 1):
			fireball_position_y = player_position_y
		else:
			fireball_position_y = np.random.randint(-150, HEIGHT + 150)

	elif(choice == 2):
		fireball_position_x = WIDTH + 150
		if(choice2 == 1):
			fireball_position_y = player_position_y
		else:
			fireball_position_y = np.random.randint(-150, HEIGHT + 150)

	elif(choice == 3):
		if(choice2 == 1):
			fireball_position_x = player_position_x
		else:
			fireball_position_x = np.random.randint(-150, WIDTH + 150)

		fireball_position_y = -150
	else:
		if(choice2 == 1):
			fireball_position_x = player_position_x
		else:
			fireball_position_x = np.random.randint(-150, WIDTH + 150)
		
		fireball_position_y = HEIGHT + 150

	fireball_angle = int((math.degrees(math.atan2((fireball_position_y - player_position_y), (player_position_x - fireball_position_x))) + 180) % 360)
	return Fireball(fireball_position_x, fireball_position_y, fireball_angle)


def generatePlayer():
	return Player(WIDTH/2, HEIGHT/2)

def runGame(FPS, clock):
	run = True	
	best_fireballs_survived = 0
	quantity_fireballs = 5
	quantity_players = 1
	population = 1000
	percentage = 1
	reduction = 0.05
	highest_wave = 0
	wave = [0 for i in range(population)]
	players = [generatePlayer() for i in range(population)]
	fireballs = [[generateFireball2(players[i].rect.center[0], players[i].rect.center[1]) for j in range(quantity_fireballs)] for i in range(population)]
	neural_networks = [NeuralNetwork(6*quantity_fireballs, 4, 4, 4) for i in range(population)]
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

		# GENERATE NEW PLAYERS IF ALL DEAD

		if(len(players) == 0):
			print(percentage)

			if(percentage < reduction):
				ercentage = reduction/5
				reduction = reduction/10.0
			else:
				percentage = percentage - reduction
			
			print(best_neural_networks[-1].wih1)	
			print(best_neural_networks[-1].wh1h2)
			print(best_neural_networks[-1].wh2o)

			wave = [0 for i in range(population)]			
			players = [generatePlayer() for i in range(population)]
			fireballs = [[generateFireball2(players[i].rect.center[0], players[i].rect.center[1]) for j in range(quantity_fireballs)] for i in range(population)]	
			neural_networks = [NeuralNetwork(6*quantity_fireballs, 4, 4, 4) for i in range(population)]
			for i in range(len(neural_networks)):
				neural_networks[i].generateWeightsFromParent(best_neural_networks[i%len(best_neural_networks)], percentage)
				

			best_neural_networks = []

		# GENERATE FIREBALLS

		for i in range(len(fireballs)):
			if(len(fireballs[i]) == 0):
				wave[i] += 1
				if(wave[i] > highest_wave):
					highest_wave = wave[i]

				fireballs[i] = [generateFireball2(players[i].rect.center[0], players[i].rect.center[1]) for j in range(quantity_fireballs)]

		
		# PLAYER MOVEMENT

		for player_index, player in enumerate(players):
			player_position_x, player_position_y = player.rect.center
			final_output = [0, 0, 0, 0]
			inputs = []

			

			for fireball_index, fireball in enumerate(fireballs[player_index]):

				fireball_position_x, fireball_position_y = fireball.rect.center
				distance_x = player_position_x - fireball_position_x
				distance_y = player_position_y - fireball_position_y
				distance = (distance_x**2 + distance_y**2)**(1/2)
				distance_angle = int((math.degrees(math.atan2(distance_y, distance_x)) + 180)%360)
				distance_angle = math.radians(distance_angle)
				distance_to_left_wall = player_position_x
				distance_to_right_wall = WIDTH - player_position_x
				distance_to_top_wall = player_position_y - HEIGHT*0.34
				distance_to_bottom_wall = HEIGHT - player_position_y
				fireball_angle = math.radians(fireball.angle)
				distance_to_center = ((player_position_y - (HEIGHT+0.34*HEIGHT)/2)**2 +  (player_position_x - WIDTH/2) **2)**(1/2)
				distance_to_center_angle = int(math.degrees(math.atan2(player_position_y - (HEIGHT+0.34*HEIGHT)/2, player_position_x - WIDTH/2)) + 180)%360
				distance_to_center_angle = math.radians(distance_to_center_angle)

				inputs.append(math.cos(distance_to_center_angle))
				inputs.append(math.sin(distance_to_center_angle))
				inputs.append(math.cos(distance_angle))
				inputs.append(math.sin(distance_angle))
				inputs.append(math.cos(fireball_angle))
				inputs.append(math.sin(fireball_angle))
				
	
			outputs = neural_networks[player_index].predict(inputs, quantity_fireballs)

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
			for fireball_index, fireball in enumerate(fireballs[player_index]):

				if(player.collidedWith(fireball)): #or player.collidedWithWall()):
					highest_wave = wave[player_index]	
					to_remove.append(player_index)
					break

		# REMOVE COLLIDED PLAYERS

		for index in reversed(to_remove):

			if(len(players) <= 0.01*population):
				best_neural_networks.append(neural_networks[index])

			del players[index]
			del neural_networks[index]
			del fireballs[index]
			del wave[index]

		# MOVE FIREBALL

		to_remove = []

		for i in range(len(fireballs)):
			for fireball_index, fireball in enumerate(fireballs[i]):
				fireballs[i][fireball_index].move()

				if(fireball.not_in_the_screen):
					to_remove.append([i, fireball_index])
					
		for indexes in reversed(to_remove):
			del fireballs[indexes[0]][indexes[1]]




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