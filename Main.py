# -*- encoding: utf-8 -*-
import numpy as np
import cv2
from tkinter.filedialog import askopenfilename

import Scene
import Object
import Util

sceneFile = askopenfilename(filetypes=[("Scene Files","*.sdl")])
scene = Scene.Scene(sceneFile)

print(scene)

print(Util.cross_3d([2, 4, 5, 1], [1, 4, 2, 1], [1, 7, 4, 1]))
print(np.cross(np.subtract([2, 4, 5], [1, 4, 2]), np.subtract([2, 4, 5], [1, 7, 4])))

print(Util.distancia_pontos([2, 4, 5], [1, 4, 2]))

novaReta = Util.row_points_planes([2, 4, 5, 1], [1, 4, 2, 1])
print(novaReta)
print(np.dot(novaReta[0], [2, 4, 5, 1]), Util.eq(np.dot(novaReta[0], [2, 4, 5, 1]), 0))
print(np.dot(novaReta[0], [1, 4, 2, 1]), Util.eq(np.dot(novaReta[0], [1, 4, 2, 1]), 0))
print(np.dot(novaReta[1], [2, 4, 5, 1]), Util.eq(np.dot(novaReta[1], [2, 4, 5, 1]), 0))
print(np.dot(novaReta[1], [1, 4, 2, 1]), Util.eq(np.dot(novaReta[1], [1, 4, 2, 1]), 0))
print(Util.row_points_planes(novaReta[0], novaReta[1]))

img = np.zeros([scene.size[0], scene.size[1], 3])
img[50, 20:100, 0] = 255
img[100, 20:100, 1] = 255
img[120, 20:100, 2] = 255

Util.showimg("Teste", img)
cv2.waitKey(0)
cv2.destroyAllWindows()