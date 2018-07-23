# -*- encoding: utf-8 -*-
import numpy as np
import Util

class Object:
	def __init__(self, filename):
		self.v = []
		tempF = []
		with open(filename) as f:
			for l in f:
				line = l[:-1].split(" ")
				if (line[0] == "v"):
					newVertex = list(map(float, line[1:]))
					newVertex.append(1)
					self.v.append(newVertex)
				elif (line[0] == "f"):
					tempF.append(list(map(int, line[1:])))
		self.triangle = [self.get_triangles(x) for x in tempF]
		self.n = list(map(self.get_normals, self.triangle))
	
	def __str__(self):
		'''Esse metodo é chamado em print(object)'''
		return "Object(\n\tv = " + str(self.v) + "\n\tnormais = " + str(self.n) + "\n\ttriangles = " + str(self.triangle) + "\n)"
	
	def get_triangles(self, d):
		'''Retorna os triangulos'''
		return np.array([self.v[d[0] - 1], self.v[d[1] - 1], self.v[d[2] - 1]])
	
	def get_normals(self, d):
		'''Retorna as normais dos triângulos'''
		return Util.normalize_w(Util.cross_3d(d[0], d[1], d[2]))