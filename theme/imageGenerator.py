from PIL import Image
import numpy as np
import sys
from typing import List
sys.path.append("../mainapp/")
import caller


def gen_image(modules: bool = False, stations: bool = False):
    arr = caller.getTestMap()
    larr = len(arr)
    data = np.zeros((larr, larr, 3), dtype=np.uint8)
    for i in range(larr):
        for j in range(larr):
            data[i, j] = [arr[i][j], 0, 0]
    img = Image.fromarray(data)
    img.save("templates/map.png")
    img.show()
gen_image()
