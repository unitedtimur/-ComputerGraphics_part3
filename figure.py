from typing import List, Union, Any

VERTEXES: List[Union[List[int], List[Union[int, float]]]] = [
    [0, 0, 0],
    [5, 0, 0],
    [0, 5, 0],
    [0, 0, 5],
    [0, 2, 1.5],
    [0, -2, 1.5],
    [0, -2, -1.5],
    [0, 2, -1.5],
    [2, 0, 1.5],
    [2, 0, -1.5]]

EDGES: List[Union[List[int], Any]] = [[
    0, 1],
    [0, 2],
    [0, 3]]

FACES: List[List[int]] = [
    [4, 5, 8],
    [5, 6, 9, 8],
    [8, 4, 7, 9],
    [4, 5, 6, 7],
    [6, 9, 7]]
