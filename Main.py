# -*- encoding: utf-8 -*-
import numpy as np
import cv2
import time

from tkinter.filedialog import askopenfilename

import Scene
import Object
import Util

# Pegando o nome do arquivo
sceneFile = askopenfilename(filetypes=[("Scene Files","*.sdl")])
scene = Scene.Scene(sceneFile)

print(scene)

# Execução do path tracing
img = scene.path_tracing()

# Funções do opencv
Util.showimg("Teste", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

Util.writeimg(scene.output, img)