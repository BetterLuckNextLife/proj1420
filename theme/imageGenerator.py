from PIL import Image
import numpy as np
import sys
from pprint import pp
from typing import List
sys.path.append("../mainapp/")
import caller

def remap(l: List[int]) -> List[int]:
    return list(map(lambda x: (x,0,0), l))


def gen_image():
    arr = caller.getTestMap()
    data = np.zeros((64, 64, 3), dtype=np.uint8)
    for i in range(64):
        for j in range(64):
            data[i, j] = [arr[i][j], 0, 0]
    img = Image.fromarray(data)
    img.save("templates/map.png")
    img.show()
gen_image()
