# -*- encoding: utf-8 -*-
import numpy as np
import Object
import Util

import time

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
					self.eye.append(1)
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
		'''Esse metodo é chamado em print(scene).'''
		return "Scene(\n\toutput = " + self.output + "\n\teye = " + str(self.eye) + "\n\tortho = " + str(self.ortho) + "\n\tsize = " + str(self.size) + "\n\tbackground = " + str(self.background) + "\n\tambient = " + str(self.ambient) + "\n\tlight = " + str(self.light) + "\n\tnpaths = " + str(self.npaths) + "\n\ttonemapping = " + str(self.tonemapping) + "\n\tseed = " + str(self.seed) + "\n\tobject = " + str(self.object) + "\n)"
	
	def scale_screen_camera(self, x, y):
		'''Converte pontos na tela em pontos na cena.'''
		tX = x / (self.size[0] - 1)
		tY = y / (self.size[1] - 1)
		return [(1 - tX) * self.ortho[0] + tX * self.ortho[2], (1 - tY) * self.ortho[3] + tY * self.ortho[1], 0, 1]
	
	def gen_ray_vectors(self):
		'''Gera as direções dos raios de cada pixel da tela, selecionando um ponto no plano da tela.'''
		output = np.zeros([self.size[0], self.size[1], 4])
		for x in range(output.shape[0]):
			for y in range(output.shape[1]):
				output[x, y, :] = self.scale_screen_camera(x, y)
		return output
	
	def path_tracing(self):
		'''O código do path tracing vai aqui.'''
		img = np.zeros([self.size[0], self.size[1], 3])
		tempTime = time.time()
		vectors = self.gen_ray_vectors()
		print("Obter pontos:", time.time() - tempTime)
		
		test1 = [1, 0, -2, 1]
		test2 = [-1, 0, -1, 1]
		test3 = [0, 1, -1, 1]
		testtriangle = Util.cross_3d(test1, test2, test3)
		
		planeTime = 0
		triangleTime = 0
		
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				# Planos gerados do raio da camera
				tempTime = time.time()
				planes = Util.row_points_planes(self.eye, vectors[x, y, :])
				planeTime += time.time() - tempTime
				# print(planes)
				
				point = Util.normalize_w(Util.cross_3d(planes[0], planes[1], testtriangle))[:-1]
				# print(point)
				
				tempTime = time.time()
				if Util.inside_triangle(test1[:-1], test2[:-1], test3[:-1], point):
					img[x, y, :] = [255, 255, 255]
				triangleTime += time.time() - tempTime
		
		print("Geração de planos", planeTime)
		print("Checagem de triangulos", triangleTime)
		
		return img