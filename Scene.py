# -*- encoding: utf-8 -*-
import numpy as np
import math
import random
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
					self.ambient = float(line[1])
				elif line[0] == "light":
					newLight = [Object.Object("Objects/" + line[1])]
					newLight.extend([float(i)*float(line[-1]) for i in line[2:-1]])
					self.light.append(newLight)
				elif line[0] == "npaths":
					self.npaths = int(line[1])
				elif line[0] == "tonemapping":
					self.tonemapping = float(line[1])
				elif line[0] == "seed":
					self.seed = int(line[1])
				elif line[0] == "object":
					newObject = [Object.Object("Objects/" + line[1])]
					newObject.extend([float(i) for i in line[2:]])
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
	
	def trace_path(self, x, y):
		'''Traça um raio correspondente às coordenadas x e y da tela.'''
		# Planos gerados do raio da camera
		planes = Util.row_points_planes(self.eye, self.vectors[x, y, :])
		# print(planes)
		
		for reflex in range(3):
		
			# Objeto mais próximo que colidiu com raio e distância
			minDist = math.inf
			hitObj = None
			hitLight = False
			
			# Colisões com sólidos
			for solid in self.object:
				solidObj = solid[0]
				for i in range(len(solidObj.triangle)):
					point = Util.normalize_w(Util.cross_3d(planes[0], planes[1], solidObj.n[i]))
					
					if Util.inside_triangle(solidObj.triangle[i], point):
						if Util.distance(self.eye, point) < minDist:
							hitObj = solid
							minDist = Util.distance(self.eye, point)
			
			# Colisões com luzes
			for light in self.light:
				lightObj = light[0]
				for i in range(len(lightObj.triangle)):
					point = Util.normalize_w(Util.cross_3d(planes[0], planes[1], lightObj.n[i]))
					
					if Util.inside_triangle(lightObj.triangle[i], point):
						if Util.distance(self.eye, point) < minDist:
							hitLight = True
							hitObj = light
							minDist = Util.distance(self.eye, point)
			
			# Ilumina com a cor do objeto mais próximo
			if (hitObj != None):
				if hitLight:
					self.img[x, y, :] = hitObj[1:4]
					break
				else:
					# Ambiente
					self.img[x, y, :] += np.dot(hitObj[1:4], self.ambient * hitObj[4])
					# kChoice = random.random() * np.sum(hitObj[5:8])
					# Difuso
					# if kChoice < hitObj[5]:
					# Especular
					# elif kChoice < hitObj[6] + hitObj[7]:
					# Transparência
					# else:
			else:
				if reflex == 0:
					self.img[x, y, :] = self.background
				break
		
		print(x)
	
	def path_tracing(self):
		'''O código do path tracing vai aqui.'''
		self.img = np.zeros([self.size[0], self.size[1], 3])
		self.vectors = self.gen_ray_vectors()
		
		random.seed(self.seed)
		totalTime = time.time()
		
		for x, y in np.ndindex((self.size[0], self.size[1])):
			self.trace_path(x, y)
		
		print("Execução total", time.time() - totalTime)
		
		return self.img