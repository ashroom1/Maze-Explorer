from random import choice, shuffle, randrange
from heapq import heappush, heappop
import sys

WALL = 100
INFINITY = 9999


class Explorer:

    def __init__(self, x, y, gx, gy):
        self.x = x
        self.y = y
        self.goalx = gx
        self.goaly = gy
        self.maxdim = min(50, 2 * max(gx, gy))
        self.mazemap = {}
        self.vlist = []
        for i in range(self.maxdim):
            for j in range(self.maxdim):
                self.mazemap[(i, j)] = [True, True, True, True]
                self.vlist.append((i, j))
        for i in range(self.maxdim):
            self.mazemap[(i, 0)][1] = False
            self.mazemap[(i, self.maxdim - 1)][3] = False
            self.mazemap[(0, i)][2] = False
            self.mazemap[(self.maxdim - 1, i)][0] = False
        self.path = list(self.pathfinder())

    def pathfinder(self):
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        u = (self.x, self.y)
        w = (self.goalx, self.goaly)
        pq = [(0, u, ())]  # one element heap, with items = (distance, vertex, path to vertex)
        visited = set()  # visited = empty set
        mindist = {u: 0}  # mindist = dictionary, key = vertex, value = distance
        while pq:
            (dist, u, path) = heappop(pq)
            if u not in visited:
                visited.add(u)
                path = (u, *path)
                if u == w:
                    #              print(w)
                    #              print(path)
                    #              input("? ")
                    return list(path)
                for i in range(4):
                    if not self.mazemap[u][i]:
                        continue
                    v = (u[0] + dx[i], u[1] + dy[i])
                    if v in visited:
                        continue
                    pdist = mindist.get(v, None)
                    ndist = dist + 1
                    if pdist == None or ndist < pdist:
                        mindist[v] = ndist
                        heappush(pq, (ndist, v, path))
        print('pathfinder failure')
        print(self.x, self.y)
        print(w)
        print(path)
        sys.exit(0)

    def update(self, m):
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]

        self.x += dx[m]
        self.y += dy[m]
        self.lastmove = m

    def action(self):
        revdir = {(1, 0): 0, (0, -1): 1, (-1, 0): 2, (0, 1): 3}
        while True:
            #        print(self.path)
            u = self.path.pop()
            v = self.path[-1]
            delta = (v[0] - u[0], v[1] - u[1])
            m = revdir[delta]
            #        print(u,v,delta,m)
            if self.view[m] == 0:
                break
            self.mazemap[u][m] = False
            self.mazemap[v][(m + 2) % 4] = False
            self.path = list(self.pathfinder())
        self.update(m)
        return [2, m]

    def feedback(self, view):
        self.view = view
