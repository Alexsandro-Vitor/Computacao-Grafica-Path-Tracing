# -*- encoding: utf-8 -*-
import numpy as np
import numpy.linalg as alg
import cv2

def eq(a, b):
	return abs(a - b) < 0.000001

def cross_3d(a, b, c):
	'''Produto cruzado para 3 pontos 4D (o cross do numpy só vai até 3D, então tive que fazer)'''
	i = np.array([a[1:], b[1:], c[1:]])
	j = np.array([[a[2], a[3], a[0]], [b[2], b[3], b[0]], [c[2], c[3], c[0]]])
	k = np.array([[a[3], a[0], a[1]], [b[3], b[0], b[1]], [c[3], c[0], c[1]]])
	l = np.array([a[:-1], b[:-1], c[:-1]])
	return [alg.det(i), -alg.det(j), alg.det(k), -alg.det(l)]

def row_points_planes(a, b):
	if eq(a[0], b[0]) and eq(a[1], b[1]):
		return ([1, 0, 0, 0], [0, 1, 0, 0])
	planeA = np.cross(np.subtract(a, b), [0, 0, 1, 1])
	planeB = np.cross(np.subtract(a, b), planeB)
	return (planeA, planeB)

def showimg(title, img):
	'''Como o opencv usa (y, x) como ordem das coordenadas e [blue, green, red] como ordem das cores, essa função é usada para visualizar uma matriz mais "convencional" como uma imagem do opencv.'''
	r,g,b = cv2.split(img)
	r = np.transpose(r)
	g = np.transpose(g)
	b = np.transpose(b)
	cv2.imshow(title, cv2.merge((b,g,r)))