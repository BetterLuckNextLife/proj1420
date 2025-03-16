from PIL import Image
import numpy as np
import sys
sys.path.append("../mainapp/")
import caller


def gen_image(modules: bool = False, stations: bool = False, coords: bool = False) -> None:
    '''gen_image(modules: bool = False, stations: bool = False, coords: bool = False)
        example: gen_image(True)
    '''
    arr = caller.getFullMap()
    larr = 256
    data = np.zeros((larr, larr, 3), dtype=np.uint8)
    for tile in range(4):
        for tile2 in range(4):
            for i in range(64):
                for j in range(64):
                    data[tile*64+i, tile2*64+j] = [arr[tile2+tile][i][j], 0, 0]
    img = Image.fromarray(data)
    img.save("templates/map.png")


if __name__ == "__main__":
    gen_image()

