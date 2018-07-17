# -*- encoding: utf-8 -*-
import numpy as np
import Object

class Scene:
	def __init__(self, filename):
		self.light = []
		self.object = []
		with open(filename) as f:
			for l in f:
				line = l[:-1].split(" ")
				if line[0] == "output":
					self.output = line[1]
				elif line[0] == "eye":
					self.eye = list(map(float, line[1:]))
				elif line[0] == "ortho":
					self.ortho = list(map(float, line[1:]))
				elif line[0] == "size":
					self.size = list(map(int, line[1:]))
				elif line[0] == "background":
					self.background = list(map(float, line[1:]))
				elif line[0] == "ambient":
					self.ambient = line[1]
				elif line[0] == "light":
					newLight = [Object.Object("Objects/" + line[1])]
					newLight.extend(list(map(float, line[2:])))
					self.light.append(newLight)
				elif line[0] == "npaths":
					self.npaths = line[1]
				elif line[0] == "tonemapping":
					self.tonemapping = line[1]
				elif line[0] == "seed":
					self.seed = line[1]
				elif line[0] == "object":
					newObject = [Object.Object("Objects/" + line[1])]
					newObject.extend(list(map(float, line[2:])))
					self.object.append(newObject)
	
	def __str__(self):
		'''Esse metodo é chamado em print(scene)'''
		return "Scene(\n\toutput = " + self.output + "\n\teye = " + str(self.eye) + "\n\tortho = " + str(self.ortho) + "\n\tsize = " + str(self.size) + "\n\tbackground = " + str(self.background) + "\n\tambient = " + str(self.ambient) + "\n\tlight = " + str(self.light) + "\n\tnpaths = " + str(self.npaths) + "\n\ttonemapping = " + str(self.tonemapping) + "\n\tseed = " + str(self.seed) + "\n\tobject = " + str(self.object) + "\n)"
	
	def scale_screen_camera(self, x, y):
		'''Converte pontos na tela em pontos na cena'''
		tX = x / (self.size[0] - 1)
		tY = y / (self.size[1] - 1)
		return [(1 - tX) * self.ortho[0] + tX * self.ortho[2], (1 - tY) * self.ortho[3] + tY * self.ortho[1], 0]
	
	def gen_ray_vectors(self):
		'''Gera as direções dos raios de cada pixel da tela'''
		output = np.zeros([self.size[0], self.size[1], 3])
		for x in range(output.shape[0]):
			for y in range(output.shape[1]):
				output[x, y, :] = np.subtract(self.scale_screen_camera(x, y), self.eye)
		return output
	
	def path_tracing(self):
		'''O código do path tracing vai aqui'''
		img = np.zeros([self.size[0], self.size[1], 3])
		return img