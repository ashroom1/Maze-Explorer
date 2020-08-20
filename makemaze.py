import sys
from random import randrange, shuffle


class Maze:

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        print(cols, rows)
        self.make_grid()
        x = randrange(self.cols)
        y = randrange(self.rows)
        self.knockdown(x, y)
        for _ in range((self.rows * self.cols) // 4):
            x = randrange(1, self.cols - 1)
            y = randrange(1, self.rows - 1)
            self.knockdownmore(x, y)

    def make_grid(self):

        wall = {}
        visited = {}
        for i in range(self.cols):
            for j in range(self.rows):
                wall[(i, j)] = [True, True, True, True]
                visited[(i, j)] = False

        self.wall = wall
        self.visited = visited

    def knockdown(self, x, y):
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        dirs = [0, 1, 2, 3]
        shuffle(dirs)
        self.visited[(x, y)] = True;
        for d1 in dirs:
            d2 = (d1 + 2) % 4
            if self.wall[(x, y)][d1]:
                nx = x + dx[d1]
                if nx < 0 or nx >= self.cols:
                    continue
                ny = y + dy[d1]
                if ny < 0 or ny >= self.rows:
                    continue
                if not self.visited[(nx, ny)]:
                    self.wall[(x, y)][d1] = False
                    self.wall[(nx, ny)][d2] = False
                    self.knockdown(nx, ny)

    def knockdownmore(self, x, y):
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        dirs = [0, 1, 2, 3]
        shuffle(dirs)
        self.visited[(x, y)] = True;
        for d1 in dirs:
            d2 = (d1 + 2) % 4
            if self.wall[(x, y)][d1]:
                nx = x + dx[d1]
                ny = y + dy[d1]
                self.wall[(x, y)][d1] = False
                self.wall[(nx, ny)][d2] = False
                return

    def getwalls(self):
        return self.wall


if __name__ == '__main__':

    cols = 6
    rows = 4

    maze = Maze(cols, rows)
    walls = maze.getwalls()
    for x in range(cols):
        for y in range(rows):
            print(x, y, walls[(x, y)])
