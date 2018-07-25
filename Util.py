# -*- encoding: utf-8 -*-
import cv2
import numpy as np
import numpy.linalg as LA
import functools
import math

def eq(a, b):
	return abs(a - b) < 0.000001

def magnitude(v):
	'''A norma de um vetor.'''
	return math.sqrt(functools.reduce((lambda sum, d: sum + d*d), v, 0))

def normalize(v):
	'''Normaliza um vetor.'''
	return np.divide(v, magnitude(v))

def normalize_w(v):
	'''Iguala o atributo w de um vetor P3 a 1 e escala os demais atributos proporcionalmente. Caso w == 0, faz a normalização convencional.'''
	if eq(v[3], 0):
		return np.divide(v, magnitude(v))
	else:
		return np.divide(v, v[3])

def distance(a, b):
	'''Distância entre 2 pontos.'''
	return magnitude(a - b)
	# return magnitude(np.subtract(a, b))

def cross_3d(a, b, c):
	'''Produto cruzado para 3 pontos 4D (o cross do numpy só vai até 3D, então tive que fazer).'''
	i = np.array([a[1:], b[1:], c[1:]])
	j = np.array([[a[2], a[3], a[0]], [b[2], b[3], b[0]], [c[2], c[3], c[0]]])
	k = np.array([[a[3], a[0], a[1]], [b[3], b[0], b[1]], [c[3], c[0], c[1]]])
	l = np.array([a[:-1], b[:-1], c[:-1]])
	return np.array([LA.det(i), -LA.det(j), LA.det(k), -LA.det(l)])

def row_points_planes(a, b):
	'''Converte uma reta P3 representada por 2 pontos em sua representação por 2 retas. Também faz o inverso (mas não gera necessariamente os valores anteriores).'''
	a = normalize_w(a)
	b =	normalize_w(b)
	if eq(a[0], b[0]) and eq(a[1], b[1]):
		return ([1, 0, 0, 0], [0, 1, 0, 0])
	planeA = cross_3d(a, b, np.add(a, [0, 0, 1, 1]))
	planeB = cross_3d(a, b, planeA)
	return (normalize_w(planeA), normalize_w(planeB))

def triangle_area(a, b, c):
	'''Obtem a área de um triângulo, usando a fórmula de Heron.'''
	ab = distance(a, b)
	bc = distance(b, c)
	ca = distance(c, a)
	p = (ab + bc + ca) / 2
	return math.sqrt(p * (p - ab) * (p - bc) * (p - ca))

def inside_triangle(t, p):
	'''Checa se um ponto está em um triângulo através de sua área (fórmula de Heron).'''
	if eq(p[3], 0):
		return False
	ab = distance(t[0], t[1])
	bc = distance(t[1], t[2])
	ca = distance(t[2], t[0])
	pa = distance(p, t[0])
	pb = distance(p, t[1])
	pc = distance(p, t[2])
	hP = (ab + bc + ca) / 2
	abcA = math.sqrt(abs(hP * (hP - ab) * (hP - bc) * (hP - ca)))
	hP = (pb + bc + pc) / 2
	pbcA = math.sqrt(abs(hP * (hP - pb) * (hP - bc) * (hP - pc)))
	hP = (pa + pc + ca) / 2
	apcA = math.sqrt(abs(hP * (hP - pa) * (hP - pc) * (hP - ca)))
	hP = (ab + pb + pa) / 2
	abpA = math.sqrt(abs(hP * (hP - ab) * (hP - pb) * (hP - pa)))
	return eq(abcA, pbcA + apcA + abpA)

def reflex_diffuse(Ip, kd, L, N):
	'''Reflexão difusa (NÃO TESTADO)'''
	return np.dot(Ip, kd * abs(np.dot(L, N)))

def int_pow(b, e):
	'''Potenciação com expoente inteiro (NÃO TESTADO)'''
	if e == 0:
		return 1
	if e % 2:
		return b * int_pow(b * b, e // 2)
	else:
		return int_pow(b * b, e // 2)

def reflex_specular(Ip, ks, L, N, V, n):
	'''Reflexão especular, com half vector (NÃO TESTADO)'''
	h = normalize(np.add(L, V))
	return Ip * ks * int_pow(np.dot(N, h), n)

def compose_quaternions(q1, q2):
	output = [q1[0] * q2[0] - np.dot(q1[1], q2[1])]
	output.append([a + b + c for a, b, c in zip(np.dot(q2[1], q1[0]), np.dot(q1[1], q2[0]), np.cross(q1[1], q2[1]))])
	return output

def rotate(point, q):
	vxp = np.cross(q[1], point)
	return [a + 2 * (b + c) for a, b, c in zip(point, np.dot(vxp, q[0]), np.cross(q[1], point))]

def to_opencv(img):
	'''Como o opencv usa (y, x) como ordem das coordenadas e [blue, green, red] como ordem das cores, essa função é usada para converter uma matriz mais "convencional" ara o formato do opencv.'''
	r,g,b = cv2.split(img)
	r = np.transpose(r)
	g = np.transpose(g)
	b = np.transpose(b)
	
	# Sem isso, a imagem da saída fica toda preta
	return (cv2.merge((b,g,r)) * 255).astype('uint8')