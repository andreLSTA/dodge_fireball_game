import math
import numpy as np

class NeuralNetwork:
	def __init__(self, input_nodes, hidden_nodes, output_nodes, activation="relu"):
		self.input_nodes = input_nodes
		self.hidden_nodes = hidden_nodes
		self.output_nodes = output_nodes
		self.bias = 1.0
		self.wih = np.random.randn(self.hidden_nodes, self.input_nodes + 1)*np.sqrt(2/(self.input_nodes + 1))
		self.who = np.random.randn(self.output_nodes, self.hidden_nodes + 1)*np.sqrt(2/(self.hidden_nodes + 1))
		self.activation = activation
		self.activation_functions = {
			"relu": self.relu,
			"sigmoid": self.sigmoid,
			"tanh": self.tanh
		}

	def relu(self, x):
		return max(x, 0)

	def sigmoid(self, x):
		return 1 / (1 + math.exp(-x))

	def tanh(self, x):
		return 2*NeuralNetwork.sigmoid(2*x) - 1

	def mutation(self, mutation_rate, mutation_percentage):
		
		for i in range(len(self.wih)):
			for j in range(len(self.wih[i])):
				if np.random.rand() < mutation_rate:
					v = np.random.randn()*np.sqrt(2/(self.input_nodes + 1))*mutation_percentage						
					self.wih[i][j] = self.wih[i][j] + v
					
		for i in range(len(self.who)):
			for j in range(len(self.who[i])):
				if np.random.rand() < mutation_rate:
					v = np.random.randn()*np.sqrt(2/(self.hidden_nodes + 1))*mutation_percentage
					self.who[i][j] = self.who[i][j] + v
				
	def crossover(self, parents):
		for i in range(len(self.wih)):
			for j in range(len(self.wih[i])):
				self.wih[i][j] = np.random.choice(parents).wih[i][j]
				
		for i in range(len(self.who)):
			for j in range(len(self.who[i])):
				self.who[i][j] = np.random.choice(parents).who[i][j]


	def predict(self, inputs_list):
		
		inputs_list.append(self.bias)
		inputs = np.array(inputs_list, ndmin=2).T
		
		hidden_inputs = np.dot(self.wih, inputs)
		
		hidden_outputs = []
		for hidden_input in hidden_inputs:
			hidden_outputs.append([self.activation_functions[self.activation](hidden_input)])

		hidden_outputs.append([self.bias])
		hidden_outputs = np.array(hidden_outputs)
		
		final_inputs = np.dot(self.who, hidden_outputs)
		
		final_outputs = []
		for final_input in final_inputs:
			final_outputs.append([self.activation_functions[self.activation](final_input)])

		final_outputs = np.array(final_outputs)

		boolean_output = []
		for final_output in final_outputs:
			if(final_output>0.0):
				boolean_output.append(True)
			else:
				boolean_output.append(False)

		
		return boolean_output
