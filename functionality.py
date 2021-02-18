import numpy as np


# При помощи элементарных преобразований преобразуем мировую систему координат  СКМ  в
# систему  координат  наблюдателя  СКН  в  соответствии  с определением СКН.
def CKM_to_CKH(vertex, origin):
    n = vertex.shape[0]

    vertex_ex = np.c_[vertex, np.ones(n)]

    # СКМ сдвигаем так, чтобы точка зрения стала началом координат.
    # Соответ-ствующая матрица сдвига
    T = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [-origin[0], -origin[1], -origin[2], 1]])

    S = np.array([[-1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])

    R_90x = np.array([[1, 0, 0, 0],
                      [0, 0, -1, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])

    d = np.sqrt(origin[0] ** 2 + origin[1] ** 2)

    # Особый случай:d= 0, то есть точка зрения принадлежит оси OZ.
    # В этом случае угол uне может быть вычислен (cos(u)  = y0/  0), но
    # может быть определен как угодно, то есть доопределяется положение наблюдателя
    # на оси OZ.  Положим  для  определенности u=  0,  то  есть  делаем  матрицу uy R единичной.
    if d != 0:
        R_uy = np.array([[origin[1] / d, 0, origin[0] / d, 0],
                         [0, 1, 0, 0],
                         [-origin[0] / d, 0, origin[1] / d, 0],
                         [0, 0, 0, 1]])
    else:
        R_uy = np.eye(4)

    s = np.sqrt(origin[0] ** 2 + origin[1] ** 2 + origin[2] ** 2)

    # Особый случай:s= 0, то есть точка зрения находится в начале координат СКМ.
    # В этом случае не только угол uне может быть вычислен (cos(u) = y0/ 0), но и угол w.
    # Поэтому положим для определенности w= u= 0, то есть делаем обе матрицы uyRи wxRединичными.
    if s != 0:
        R_wx = np.array([[1, 0, 0, 0],
                         [0, d / s, -origin[2] / s, 0],
                         [0, origin[2] / s, d / s, 0],
                         [0, 0, 0, 1]])
    else:
        R_wx = np.eye(4)

    V = T @ S @ R_90x @ R_uy @ R_wx

    return (vertex_ex @ V)[:, :3], s


# Построим проекцию сцены на картинную плоскость (образ сцены), то есть построим массив VerKa[8, 2],
# i-я строка которого представит координаты xk, yki-й вершины в СКК.
# Картинная плоскость проходит через начало мировой системы координат
# перпендикулярно оси зрения и расстояние до нее равно s≈ 7,8
def CKH_to_CKK(vertex, s):
    vertexCKK = vertex

    for point in vertexCKK:
        if point[2] != 0:
            point[0] *= s / point[2]
            point[1] *= s / point[2]

    return vertexCKK[:, 0:2]


# Зададим в картинной плоскости квадратное окно видимости,полуразмером
# Рк(с центром в начале СКК и краями параллельными осям СКК), выбрав окно таким,
# чтобы  проекция  полностью  поместилась  в  окне.  При  выборе полуразмера
# окна  следует  иметь  в  виду,  что  от  размера  окна  зависят
# относительные размеры проекции: чем больше окно, тем
# меньшую его часть занимает проекция.
def CKK_to_CKEi(vertex, pk, xc, yc, xe, ye):
    for point in vertex:
        point[0] *= xe / pk
        point[1] *= -ye / pk
        point[0] += xc
        point[1] += yc
    return vertex


def plane_coefficient(face, all_edges):
    e = np.array([all_edges[face[i]] for i in range(3)])

    # Вычисления коэффициентов плоскостей
    A = (e[2][1] - e[0][1]) * (e[1][2] - e[0][2]) - (e[1][1] - e[0][1]) * (e[2][2] - e[0][2])
    B = (e[1][0] - e[0][0]) * (e[2][2] - e[0][2]) - (e[2][0] - e[0][0]) * (e[1][2] - e[0][2])
    C = (e[2][0] - e[0][0]) * (e[1][1] - e[0][1]) - (e[1][0] - e[0][0]) * (e[2][1] - e[0][1])
    D = -(A * e[0][0] + B * e[0][1] + C * e[0][2])

    return np.array([A, B, C, D])


def plane_w_center(all_edges):
    edges = np.array(all_edges)
    return np.apply_along_axis(sum, 0, edges) / edges.shape[0]


def matrix_to_w_center(plane_coefficient, w_center):
    return plane_coefficient \
        if plane_coefficient[0] * w_center[0] \
           + plane_coefficient[1] * w_center[1] \
           + plane_coefficient[2] * w_center[2] \
           + plane_coefficient[3] < 0 \
        else -plane_coefficient
