# -*- encoding: utf-8 -*-
import numpy as np
import numpy.linalg as alg
import cv2
import functools
import math

def eq(a, b):
	return abs(a - b) < 0.000001

def magnitude(v):
	'''A norma de um vetor.'''
	return math.sqrt(functools.reduce((lambda sum, d: sum + d*d), v, 0))

def normalize(v):
	'''Normaliza um vetor.'''
	magnitudeV = magnitude(v)
	return list(map(lambda x: x/magnitudeV, v))

def normalize_w(v):
	'''Iguala o atributo w de um vetor P3 a 1 e escala os demais atributos proporcionalmente. Caso w == 0, faz a normalização convencional.'''
	if eq(v[3], 0):
		return normalize(v)
	else:
		return list(map(lambda x: x/v[3], v))

def distancia_pontos(a, b):
	'''Distância entre 2 pontos.'''
	return magnitude(np.subtract(a, b))

def cross_3d(a, b, c):
	'''Produto cruzado para 3 pontos 4D (o cross do numpy só vai até 3D, então tive que fazer).'''
	i = np.array([a[1:], b[1:], c[1:]])
	j = np.array([[a[2], a[3], a[0]], [b[2], b[3], b[0]], [c[2], c[3], c[0]]])
	k = np.array([[a[3], a[0], a[1]], [b[3], b[0], b[1]], [c[3], c[0], c[1]]])
	l = np.array([a[:-1], b[:-1], c[:-1]])
	return [alg.det(i), -alg.det(j), alg.det(k), -alg.det(l)]

def row_points_planes(a, b):
	'''Converte uma reta P3 representada por 2 pontos em sua representação por 2 retas. Também faz o inverso (mas não gera necessariamente os valores anteriores.'''
	a = normalize_w(a)
	b =	normalize_w(b)
	if eq(a[0], b[0]) and eq(a[1], b[1]):
		return ([1, 0, 0, 0], [0, 1, 0, 0])
	planeA = cross_3d(a, b, np.add(a, [0, 0, 1, 1]))
	planeB = cross_3d(a, b, planeA)
	return (normalize_w(planeA), normalize_w(planeB))

def triangle_area(a, b, c):
	'''Obtem a área de um triângulo'''
	ba = np.subtract(b, a)
	ca = np.subtract(c, a)
	return magnitude(np.cross(ba, ca)) / 2

def inside_triangle_area(a, b, c, p):
	'''Checa se um ponto está em um triângulo através de sua área'''
	return eq(triangle_area(a, b, c), triangle_area(p, b, c) + triangle_area(a, p, c) + triangle_area(a, b, p))

def inside_triangle_dot(a, b, c, p):
	'''Não sei se funciona, nem se é mais rápido'''
	ab = normalize(np.subtract(a, b))
	bc = normalize(np.subtract(b, c))
	ca = normalize(np.subtract(c, a))
	pa = normalize(np.subtract(p, a))
	pb = normalize(np.subtract(p, b))
	pc = normalize(np.subtract(p, c))
	return -np.dot(ca, ab) > np.dot(ca, pa) and -np.dot(ca, ab) > -np.dot(pa, ab) and -np.dot(ab, bc) > np.dot(ab, pb) and -np.dot(ab, bc) > -np.dot(pb, bc) and -np.dot(bc, ca) > np.dot(ab, pc) and -np.dot(bc, ca) > -np.dot(pc, ca)

def to_opencv(img):
	'''Como o opencv usa (y, x) como ordem das coordenadas e [blue, green, red] como ordem das cores, essa função é usada para converter uma matriz mais "convencional" ara o formato do opencv.'''
	r,g,b = cv2.split(img)
	r = np.transpose(r)
	g = np.transpose(g)
	b = np.transpose(b)
	return cv2.merge((b,g,r))

def showimg(title, img):
	'''Como o opencv usa (y, x) como ordem das coordenadas e [blue, green, red] como ordem das cores, essa função é usada para visualizar uma matriz mais "convencional" como uma imagem do opencv.'''
	cv2.imshow(title, to_opencv(img))