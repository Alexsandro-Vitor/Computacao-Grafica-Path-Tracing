# -*- encoding: utf-8 -*-
import numpy as np
import cv2
from tkinter.filedialog import askopenfilename
import Scene
import Object

sceneFile = askopenfilename(filetypes=[("Scene Files","*.sdl")])
scene = Scene.Scene(sceneFile)

# objFile = askopenfilename(filetypes=[("Object Files","*.obj")])
# object = Object.Object(objFile)
print(scene)

img = np.zeros([400, 200, 3])
img[100, 20:100, 0] = 255
img[200, 20:100, 1] = 255
img[300, 20:100, 2] = 255

def showimg(title, img):
	'''Como o opencv usa (y, x) como ordem das coordenadas e [blue, green, red] como ordem das cores, essa função é usada para visualizar uma matriz mais "convencional" como uma imagem do opencv.'''
	r,g,b = cv2.split(img)
	r = np.transpose(r)
	g = np.transpose(g)
	b = np.transpose(b)
	cv2.imshow(title, cv2.merge((b,g,r)))

showimg("Teste", img)
cv2.waitKey(0)
cv2.destroyAllWindows()