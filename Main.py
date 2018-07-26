# -*- encoding: utf-8 -*-
import numpy as np
import cv2

from tkinter.filedialog import askopenfilename

import Scene
import Object
import Util

# Pegando o nome do arquivo
sceneFile = askopenfilename(filetypes=[("Scene Files","*.sdl")])
scene = Scene.Scene(sceneFile)

# print(scene)
print(np.divide(np.array([2, 1, 3]), np.array([1, 2, -3])))

# Execução do path tracing
img = scene.path_tracing()

# Funções do opencv
img = Util.to_opencv(img)

cv2.imshow("Imagem", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite(scene.output, img)