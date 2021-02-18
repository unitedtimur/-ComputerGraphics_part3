import tkinter as tk
import numpy as np

from figure import VERTEXES, EDGES, FACES
from functionality import CKM_to_CKH, CKH_to_CKK, CKK_to_CKEi, plane_coefficient, plane_w_center, matrix_to_w_center

h = 600
w = 1200
root = tk.Tk()
cv = tk.Canvas(root, width=1200, height=600, bg='white')


class Figure:
    def __init__(self):
        self.vertexes = np.array(VERTEXES)
        self.edges = np.array(EDGES)
        self.faces = np.array(FACES, dtype=bytearray)


class DrawableFigure:
    def __init__(self, WatcherPoint):
        self.figure = Figure()
        self.x = WatcherPoint[0]
        self.y = WatcherPoint[1]
        self.z = WatcherPoint[2]
        self.lines = []
        self.polys = []
        self.W = []
        self.w_center = None

        cv.pack()

        self.angle = 0.0

        def key(event):
            if event.char == 'a':
                self.move(event, [-1, 0, 0])
            elif event.char == 'd':
                self.move(event, [1, 0, 0])
            elif event.char == 'w':
                self.move(event, [0, 1, 0])
            elif event.char == 's':
                self.move(event, [0, -1, 0])
            elif event.char == 'q':
                self.move(event, [0, 0, 1])
            elif event.char == 'e':
                self.move(event, [0, 0, -1])
            elif event.char == 'r':
                self.move(event, [self.x * 0.95 - self.x, self.y * 0.95 - self.y, self.z * 0.95 - self.z])
            elif event.char == 't':
                self.move(event, [self.x * 1.05 - self.x, self.y * 1.05 - self.y, self.z * 1.05 - self.z])

        root.bind("<Key>", lambda event: key(event))

        self.s = None

        for face in self.figure.faces:
            self.W.append(plane_coefficient(face, self.figure.vertexes))

        self.w_center = plane_w_center(self.figure.vertexes)

        self.W = np.array(self.W)
        for i in range(self.W.shape[0]):
            self.W[i] = matrix_to_w_center(self.W[i], self.w_center)

        self.drawFigure()

    def move(self, event, d):
        self.x += d[0]
        self.y += d[1]
        self.z += d[2]

        M = self.figure.vertexes
        M, s = CKM_to_CKH(M, [self.x, self.y, self.z])
        M = CKH_to_CKK(M, self.s)
        M = CKK_to_CKEi(M, 10, w / 2, h / 2, 400, 400)

        self.update(M)

    def drawFigure(self):
        M = self.figure.vertexes
        M, self.s = CKM_to_CKH(M, [self.x, self.y, self.z])
        M = CKH_to_CKK(M, self.s)
        M = CKK_to_CKEi(M, 10, w / 2, h / 2, 400, 400)

        colors = ["red", "orange", "purple", "green", "blue"]

        # Задаём полигоны
        i = 0
        for face in self.figure.faces:
            points = []
            for index in face:
                points.append(M[index][0])
                points.append(M[index][1])

            self.polys.append(cv.create_polygon(points, fill=colors[i]))
            i += 1
            # Проверяем на лицевые грани
            last = len(self.polys) - 1
            if self.W[last][0] * self.x + self.W[last][1] * self.y + self.W[last][2] * self.z + self.W[last][3] <= 0:
                cv.itemconfigure(self.polys[last], state="hidden")

        # Линии осей координат
        self.lines.append(cv.create_line(M[self.figure.edges[0][0], 0],
                                         M[self.figure.edges[0][0], 1],
                                         M[self.figure.edges[0][1], 0],
                                         M[self.figure.edges[0][1], 1], fill="red"))

        self.lines.append(cv.create_line(M[self.figure.edges[1][0], 0],
                                         M[self.figure.edges[1][0], 1],
                                         M[self.figure.edges[1][1], 0],
                                         M[self.figure.edges[1][1], 1], fill="green"))

        self.lines.append(cv.create_line(M[self.figure.edges[2][0], 0],
                                         M[self.figure.edges[2][0], 1],
                                         M[self.figure.edges[2][1], 0],
                                         M[self.figure.edges[2][1], 1], fill="blue"))

        self.lines = np.array(self.lines)
        self.polys = np.array(self.polys)

    def update(self, M):
        # Изменение проекции линий осей координат
        for i in range(3):
            cv.coords(self.lines[i], M[self.figure.edges[i][0], 0],
                      M[self.figure.edges[i][0], 1], M[self.figure.edges[i][1], 0],
                      M[self.figure.edges[i][1], 1])

        # Проверка на лицевые грани и изменение проекции видимых граней
        for i in range(self.polys.size):
            if self.W[i][0] * self.x + self.W[i][1] * self.y + self.W[i][2] * self.z + self.W[i][3] > 0:
                points = []
                for index in self.figure.faces[i]:
                    points.append(M[index][0])
                    points.append(M[index][1])

                cv.itemconfigure(self.polys[i], state="normal")
                cv.coords(self.polys[i], points)
            else:
                cv.itemconfigure(self.polys[i], state="hidden")