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

img = scene.path_tracing()

# Util.inside_triangle_dot()

# img = np.zeros([scene.size[0], scene.size[1], 3])
# img[50, 20:100, 0] = 255
# img[100, 20:100, 1] = 255
# img[120, 20:100, 2] = 255

Util.showimg("Teste", img)
cv2.waitKey(0)
cv2.destroyAllWindows()