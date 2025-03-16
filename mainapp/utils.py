import requests
import json
from PIL import Image
from caller import getFullMap
import numpy as np
leftUp = None
leftDown = None
rightUp = None
rightDown = None
def is_corner_tile(tile, corner_type):
    """
    Проверяет, является ли тайл угловым.
    :param tile: Матрица 64x64 (список списков или массив NumPy).
    :param corner_type: Тип угла ('leftUp', 'leftDown', 'rightUp', 'rightDown').
    :return: True, если тайл является угловым, иначе False.
    """
    if isinstance(tile, np.ndarray):
        tile = tile.tolist()  # Преобразуем массив NumPy в список списков

    rows = len(tile)
    cols = len(tile[0]) if rows > 0 else 0

    if corner_type == 'leftUp':
        return all(tile[i][0] == 255 for i in range(rows)) and all(tile[0][j] == 255 for j in range(cols))
    elif corner_type == 'leftDown':
        return all(tile[i][0] == 255 for i in range(rows)) and all(tile[-1][j] == 255 for j in range(cols))
    elif corner_type == 'rightUp':
        return all(tile[i][-1] == 255 for i in range(rows)) and all(tile[0][j] == 255 for j in range(cols))
    elif corner_type == 'rightDown':
        return all(tile[i][-1] == 255 for i in range(rows)) and all(tile[-1][j] == 255 for j in range(cols))
    return False
all_tiles = list(getFullMap())
for grid in all_tiles:
    if is_corner_tile(grid, 'leftUp'):
        leftUp = grid
    elif is_corner_tile(grid, 'leftDown'):
        leftDown = grid
    elif is_corner_tile(grid, 'rightUp'):
        rightUp = grid
    elif is_corner_tile(grid, 'rightDown'):
        rightDown = grid
found_tiles = {
    'leftUp': leftUp,
    'leftDown': leftDown,
    'rightUp': rightUp,
    'rightDown': rightDown
}
remaining_tiles = [tile for tile in all_tiles if tile not in found_tiles.values()]
def borders_match(tile1, tile2, side1, side2):
    if side1 == 'top':
        border1 = tile1[0]
    elif side1 == 'bottom':
        border1 = tile1[-1]
    elif side1 == 'left':
        border1 = [row[0] for row in tile1]
    elif side1 == 'right':
        border1 = [row[-1] for row in tile1]

    if side2 == 'top':
        border2 = tile2[0]
    elif side2 == 'bottom':
        border2 = tile2[-1]
    elif side2 == 'left':
        border2 = [row[0] for row in tile2]
    elif side2 == 'right':
        border2 = [row[-1] for row in tile2]

    return all(abs(b1 - b2) <= 1 for b1, b2 in zip(border1, border2))
def find_remaining_tiles(found_tiles, remaining_tiles):
    positions = {
        'top': [],
        'bottom': [],
        'left': [],
        'right': [],
        'center': []
    }

    for tile in remaining_tiles:
        if borders_match(tile, found_tiles['leftUp'], 'left', 'right'):
            positions['top'].append(tile)
        elif borders_match(tile, found_tiles['rightUp'], 'right', 'left'):
            positions['top'].append(tile)

    for tile in remaining_tiles:
        if borders_match(tile, found_tiles['leftDown'], 'left', 'right'):
            positions['bottom'].append(tile)
        elif borders_match(tile, found_tiles['rightDown'], 'right', 'left'):
            positions['bottom'].append(tile)

    for tile in remaining_tiles:
        if borders_match(tile, found_tiles['leftUp'], 'top', 'bottom'):
            positions['left'].append(tile)
        elif borders_match(tile, found_tiles['leftDown'], 'bottom', 'top'):
            positions['left'].append(tile)

    for tile in remaining_tiles:
        if borders_match(tile, found_tiles['rightUp'], 'top', 'bottom'):
            positions['right'].append(tile)
        elif borders_match(tile, found_tiles['rightDown'], 'bottom', 'top'):
            positions['right'].append(tile)

    for tile in remaining_tiles:
        if tile not in positions['top'] + positions['bottom'] + positions['left'] + positions['right']:
            positions['center'].append(tile)

    return positions

remaining_positions = find_remaining_tiles(found_tiles, remaining_tiles)
for position, tiles in remaining_positions.items():
    print(f"Позиция: {position}, количество тайлов: {len(tiles)}")


def assemble_big_square(found_tiles, remaining_positions):
    big_square = [[0 for _ in range(256)] for _ in range(256)]

    for i in range(64):
        for j in range(64):
            big_square[i][j] = found_tiles['leftUp'][i][j]

    for i in range(64):
        for j in range(192, 256):
            big_square[i][j] = found_tiles['rightUp'][i][j - 192]

    for i in range(192, 256):
        for j in range(64):
            big_square[i][j] = found_tiles['leftDown'][i - 192][j]

    for i in range(192, 256):
        for j in range(192, 256):
            big_square[i][j] = found_tiles['rightDown'][i - 192][j - 192]

    for idx, tile in enumerate(remaining_positions['top']):
        for i in range(64):
            for j in range(64 * (idx + 1), 64 * (idx + 2)):
                big_square[i][j] = tile[i][j - 64 * (idx + 1)]

    for idx, tile in enumerate(remaining_positions['bottom']):
        for i in range(192, 256):
            for j in range(64 * (idx + 1), 64 * (idx + 2)):
                big_square[i][j] = tile[i - 192][j - 64 * (idx + 1)]

    for idx, tile in enumerate(remaining_positions['left']):
        for i in range(64 * (idx + 1), 64 * (idx + 2)):
            for j in range(64):
                big_square[i][j] = tile[i - 64 * (idx + 1)][j]

    for idx, tile in enumerate(remaining_positions['right']):
        for i in range(64 * (idx + 1), 64 * (idx + 2)):
            for j in range(192, 256):
                big_square[i][j] = tile[i - 64 * (idx + 1)][j - 192]

    for idx, tile in enumerate(remaining_positions['center']):
        row = (idx // 2) * 64 + 64
        col = (idx % 2) * 64 + 64
        for i in range(64):
            for j in range(64):
                big_square[row + i][col + j] = tile[i][j]

    return big_square

big_square = assemble_big_square(found_tiles, remaining_positions)

def gen_image(modules: bool = False, stations: bool = False, coords: bool = False) -> None:
    '''gen_image(modules: bool = False, stations: bool = False, coords: bool = False)
        example: gen_image(True)
    '''
    larr = 256
    data = np.zeros((larr, larr, 3), dtype=np.int)
    for i in range(larr):
        for j in range(larr):
            data[i,j] = [big_square[i][j], 0, 0]
    img = Image.fromarray(data)
    img.save("map.png")
gen_image()
