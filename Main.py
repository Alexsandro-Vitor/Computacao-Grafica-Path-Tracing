# -*- encoding: utf-8 -*-
import numpy as np
import cv2
import time
import random

from tkinter.filedialog import askopenfilename

import Scene
import Object
import Util

# Pegando o nome do arquivo
sceneFile = askopenfilename(filetypes=[("Scene Files","*.sdl")])
scene = Scene.Scene(sceneFile)

# print(scene)

# teste = [[random.random(), random.random(), random.random()] for _ in range(1000000)]
# testRes = []
# testTime = time.time()
# for i in teste:
	# testRes.append([4.68 * x for x in i])
# print(testRes[:10])
# print("[]:", time.time() - testTime)
# testRes = []
# testTime = time.time()
# for i in teste:
	# testRes.append(Util.prod_vector_scalar(i, 4.68))
# print(testRes[:10])
# print("prod_vector_scalar:", time.time() - testTime)

# Execução do path tracing
img = scene.path_tracing()

# Funções do opencv
img = Util.to_opencv(img)

cv2.imshow("Imagem", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite(scene.output, img)