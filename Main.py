# -*- encoding: utf-8 -*-
import numpy as np
import cv2

from tkinter.filedialog import askopenfilename

import Scene
import Object
import Util

if __name__ == '__main__':
	# Pegando o nome do arquivo
	sceneFile = askopenfilename(filetypes=[("Scene Files","*.sdl")])
	scene = Scene.Scene(sceneFile)

	print(scene)

	# Execução do path tracing
	img = scene.path_tracing()

	# Funções do opencv
	img = Util.to_opencv(img)
	
	cv2.imshow("Imagem", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	
	cv2.imwrite("Results/" + scene.output, img)