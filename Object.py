# -*- encoding: utf-8 -*-
class Object:
	def __init__(self, filename):
		self.v = []
		self.f = []
		with open(filename) as f:
			for l in f:
				line = l[:-1].split(" ")
				if (line[0] == "v"):
					self.v.append(list(map(float, line[1:])))
				elif (line[0] == "f"):
					self.f.append(list(map(int, line[1:])))
	def __str__(self):
		'''Esse metodo é chamado em print(object)'''
		return "Object(\n\tv = " + str(self.v) + "\n\tf = " + str(self.f) + "\n)"