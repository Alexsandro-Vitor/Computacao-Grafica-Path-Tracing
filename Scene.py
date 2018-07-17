# -*- encoding: utf-8 -*-
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
					newLight = [line[1]]
					newLight.extend(list(map(float, line[2:])))
					self.light.append(newLight)
				elif line[0] == "npaths":
					self.npaths = line[1]
				elif line[0] == "tonemapping":
					self.tonemapping = line[1]
				elif line[0] == "seed":
					self.seed = line[1]
				elif line[0] == "object":
					newObject = [line[1]]
					newObject.extend(list(map(float, line[2:])))
					self.object.append(newObject)
	def __str__(self):
		'''Esse metodo é chamado em print(scene)'''
		return "Scene(\n\toutput = " + self.output + "\n\teye = " + str(self.eye) + "\n\tortho = " + str(self.ortho) + "\n\tsize = " + str(self.size) + "\n\tbackground = " + str(self.background) + "\n\tambient = " + str(self.ambient) + "\n\tlight = " + str(self.light) + "\n\tnpaths = " + str(self.npaths) + "\n\ttonemapping = " + str(self.tonemapping) + "\n\tseed = " + str(self.seed) + "\n\tobject = " + str(self.object) + "\n)"