# -*- encoding: utf-8 -*-
import numpy as np
import Util
import functools

class Object:
	def __init__(self, filename):
		self.v = []
		tempF = []
		with open(filename) as f:
			for l in f:
				line = l[:-1].split(" ")
				if (line[0] == "v"):
					line.append(1)
					newVertex = np.array([float(i) for i in line[1:]])
					self.v.append(newVertex)
				elif (line[0] == "f"):
					tempF.append([int(i) for i in line[1:]])
		self.triangle = np.array([self.get_triangles(i) for i in tempF])
		self.n = list(map(self.get_normals, self.triangle))
		self.centroid = self.get_centroid()
	
	def __str__(self):
		'''Esse metodo é chamado em print(object)'''
		return "Object(\n\tv = " + str(self.v) + "\n\tnormais = " + str(self.n) + "\n\ttriangles = " + str(self.triangle) + "\n)"
	
	def get_triangles(self, d):
		'''Retorna os triangulos'''
		return np.array([self.v[d[0] - 1], self.v[d[1] - 1], self.v[d[2] - 1]])
	
	def get_normals(self, d):
		'''Retorna as normais dos triângulos'''
		return Util.normalize_w(Util.cross_3d(d[0], d[1], d[2]))
	
	def get_centroid(self):
		'''Calcula o ponto central do objeto'''
		return Util.normalize_w(functools.reduce((lambda sum, d: sum + d), self.v, np.zeros(4)))