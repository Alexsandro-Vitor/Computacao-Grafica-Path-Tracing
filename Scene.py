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

	def check_colisions(self, origin, planes):
		'''Checa se um raio colide com um objeto e obtêm as características dele.'''
		# origin é o ponto de onde parte o raio
		
		# Objeto mais próximo que colidiu com raio e distância
		hitLight = False	# Colidiu com uma fonte de luz?
		hitObj = None		# Objeto que colidiu com o raio
		minDist = math.inf	# Distancia mínima (já que colide com o objeto mais próximo)
		hitPoint = None		# Ponto de colisão
		index = None		# O índice do triângulo / normal do objeto que colidiu com o raio

		# Colisões com sólidos
		for solid in self.object:
			solidObj = solid[0]
			for i in range(len(solidObj.triangle)):
				point = Util.normalize_w(Util.cross_3d(planes[0], planes[1], solidObj.n[i]))
				
				if Util.inside_triangle(solidObj.triangle[i], point):
					if Util.distance(origin, point) < minDist:
						hitObj = solid
						minDist = Util.distance(origin, point)
						hitPoint = point
						index = i

		# Colisões com luzes
		for light in self.light:
			lightObj = light[0]
			for i in range(len(lightObj.triangle)):
				point = Util.normalize_w(Util.cross_3d(planes[0], planes[1], lightObj.n[i]))

				if Util.inside_triangle(lightObj.triangle[i], point):
					if Util.distance(origin, point) < minDist:
						hitLight = True
						hitObj = light
						minDist = Util.distance(origin, point)
						hitPoint = point
						index = i
				return (hitLight, hitObj, minDist, hitPoint, index)

	def trace_path(self, x, y):
		'''Traça um raio correspondente às coordenadas x e y da tela.'''
		
		# Cores geradas em cada path
		colors = np.zeros((self.npaths, 3))
		
		for path in range(self.npaths):
			# Planos gerados do raio da camera
			oldPoint = self.eye
			planes = Util.row_points_planes(oldPoint, self.vectors[x, y, :])
			for reflex in range(3):
				(hitLight, hitObj, minDist, hitPoint, index) = self.check_colisions(oldPoint, planes)

				# Ilumina com a cor do objeto mais próximo
				if (hitObj != None):
					if hitLight:
						colors[path] += hitObj[1:4]
						break
					else:
						# Ambiente
						colors[path] += np.dot(hitObj[1:4], self.ambient * hitObj[4])
						
						# Raio secundário
						normal = hitObj[0].n[index][:-1]
						if np.dot(normal, np.subtract(oldPoint[:-1], hitPoint[:-1])) < 0:
							normal = np.dot(normal, -1)
						# print("v:", np.subtract(oldPoint[:-1], hitPoint[:-1]))
						# print("normal:", normal)
						phi = math.acos(math.sqrt(random.random()))
						theta = math.pi * random.random()
						q1 = [math.cos(phi / 2), np.dot(np.subtract(hitObj[0].triangle[index][0][:-1], hitPoint[:-1]), math.sin(phi / 2))]
						# print("q1:", q1)
						q2 = [math.cos(theta), np.dot(normal, math.sin(theta))]
						# print("q2:", q2)
						qComposed = Util.compose_quaternions(q2, q1)
						# print("qComposed:", qComposed)
						newVector = Util.normalize(Util.rotate(normal, qComposed))
						newVector = np.array([newVector[0], newVector[1], newVector[2], 1])
						# print(newVector)
						
						# Shadow ray
						#chosenLight = random.choice(self.light)
						#chosenPoint = random.choice(chosenLight[0].v)
						#shadowRay = Util.normalize(hitPoint[:-1] - chosenPoint[:-1])

						# Falta fazer a função que selecionará as luzes que são vistar pelo ponto
						chosenLight = self.light[0]
						shadowRay = Util.shadow_rays(chosenLight[0].v, hitPoint);
						
						# if np.dot(normal, shadowRay) < 0:
							# shadowRay = np.dot(shadowRay, -1)
						
						kChoice = random.random() * np.sum(hitObj[5:8])
						# Difuso
						if kChoice < hitObj[5]:
							colors[path] += Util.reflex_diffuse(chosenLight[1:], hitObj[5], shadowRay, normal)
						# Especular
						elif kChoice < hitObj[6] + hitObj[7]:
							colors[path] += Util.reflex_specular(chosenLight[1:], hitObj[6], shadowRay, normal, oldPoint, hitObj[8])
							
						# Transparência
						# else:
						
						
						# Atualiza essas variáveis somente no final
						oldPoint = hitPoint
						planes = Util.row_points_planes(oldPoint, np.add(hitPoint, newVector))
						# print(planes)
				else:
					if reflex == 0:
						colors[path, :] = self.background
					break

			break
		
		# print(x)
		
		return colors[0]
		#return [(float(total) / (self.npaths * 3)) for total in reduce(lambda x, y: [x[0] + y[0], x[1] + y[1], x[2] + y[2]], colors)]
	
	def path_tracing(self):
		'''O código do path tracing vai aqui.'''
		self.img = np.zeros([self.size[0], self.size[1], 3])
		self.vectors = self.gen_ray_vectors()
		
		random.seed(self.seed)
		totalTime = time.time()
		
		for x, y in np.ndindex((self.size[0], self.size[1])):
			self.img[x, y, :] = self.trace_path(x, y)
		
		print("Execução total", time.time() - totalTime)
		
		return self.img
