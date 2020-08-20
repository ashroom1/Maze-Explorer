import sys
import time
from random import randrange, shuffle
from tkinter import *
from makemaze import Maze

# Your module goes here: explorerXX

from explorerE08 import Explorer as Explorer1

NPLAYER = 1
BORDER = 10
XUNIT = 72
YUNIT = 72
RAD = 15
GAMEWID = 8
GAMEHGT = 8
RECT = 30

WALL = 100

colorlist = ['blue', 'purple2', 'orange', 'slategray']

ExplorerList = [Explorer1]


class Player:

    def __init__(self, game, pno):
        self.pno = pno + 101
        self.game = game
        self.lab = game.lablist[pno]
        self.brd = game.board
        self.ticks = 0
        self.lab.configure(text=str(0))
        self.x = 0
        self.y = 0
        self.brd[self.x][self.y] = self.pno
        self.px = BORDER + self.x * XUNIT + XUNIT // 2
        self.py = BORDER + self.y * YUNIT + YUNIT // 2
        self.me = game.can.create_oval(self.px - RAD, self.py - RAD, self.px + RAD, self.py + RAD, fill=colorlist[pno])

    def move(self, x, y):
        self.brd[x][y] = self.pno
        self.brd[self.x][self.y] = 0
        self.x = x
        self.y = y
        self.px = BORDER + x * XUNIT + XUNIT // 2
        self.py = BORDER + y * YUNIT + YUNIT // 2
        self.game.can.coords(self.me, self.px - RAD, self.py - RAD, self.px + RAD, self.py + RAD)
        self.ticks += 1
        self.lab.configure(text=str(self.ticks))


class Game:

    def __init__(self, win, rows, cols):
        self.win = win
        self.win.option_add("*font", ("Helvetica", 36))
        self.win.title("Maze")

        self.rows = rows
        self.cols = cols
        self.xunit = XUNIT
        self.yunit = YUNIT
        self.wid = cols * self.xunit + 2 * BORDER
        self.hgt = rows * self.yunit + 2 * BORDER
        self.wallwidth = 3

        self.dataframe = Frame(win)
        self.dataframe.pack(side='left')
        self.gfxframe = Frame(win)
        self.gfxframe.pack(side='left')
        self.ctlframe = Frame(win)
        self.ctlframe.pack(side='left')

        self.lablist = []
        for i in range(NPLAYER):
            Label(self.dataframe, text='Player ' + str(i + 1), fg=colorlist[i]).pack(side='top')
            lab = Label(self.dataframe, text='0')
            lab.pack(side='top')
            self.lablist.append(lab)

        self.can = Canvas(self.gfxframe, width=self.wid, height=self.hgt, bg='#50c878')  # or wheat
        self.can.pack()

        self.target = (randrange(rows // 2, rows - 1), randrange(cols // 2, cols - 1))
        x = BORDER + self.xunit * self.target[0] + self.xunit // 2
        y = BORDER + self.yunit * self.target[1] + self.yunit // 2
        self.can.create_rectangle(x - RECT, y - RECT, x + RECT, y + RECT, fill='red')
        Button(self.ctlframe, text='Start', command=self.automate).pack(side='top', fill=X)
        Button(self.ctlframe, text='Stop', command=self.stop).pack(side='top', fill=X)
        Button(self.ctlframe, text='Quit', command=win.quit).pack(side='top', fill=X)
        Button(self.ctlframe, text='Reset', command=self.reset).pack(side='top', fill=X)

        self.win.option_add("*Radiobutton.font", ("Helvetica", 24))
        self.ticker = IntVar()
        self.ticker.set(250)
        Radiobutton(self.ctlframe, text="Speed:   25", indicatoron=False, variable=self.ticker,
                    value=25).pack(side='top', fill=X)
        Radiobutton(self.ctlframe, text="Speed:  100", indicatoron=False, variable=self.ticker,
                    value=100).pack(side='top', fill=X)
        Radiobutton(self.ctlframe, text="Speed:  250", indicatoron=False, variable=self.ticker,
                    value=250).pack(side='top', fill=X)
        Radiobutton(self.ctlframe, text="Speed: 1000", indicatoron=False, variable=self.ticker,
                    value=1000).pack(side='top', fill=X)

        self.running = False
        self.turn = 0

        tmp = Maze(cols, rows)
        self.wall = tmp.getwalls()
        self.make_grid()

        self.starting = True
        self.reset()
        self.starting = False

    def reset(self):
        self.running = False
        self.win.after_cancel(self.playgame)

        if not self.starting:
            for i in range(NPLAYER):
                self.can.delete(self.player[i].me)
                self.player[i].move(0, 0)

        self.board = []
        for i in range(self.cols):
            self.board.append([0 for j in range(self.rows)])

        self.player = []
        for i in range(NPLAYER):
            self.player.append(Player(self, i))

        self.explorer = [None] * NPLAYER
        for i in range(NPLAYER):
            self.explorer[i] = ExplorerList[i](0, 0, self.target[0], self.target[1])

    def getview(self, x, y):
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        vw = []
        for i in range(4):
            if self.wall[(x, y)][i]:
                vw.append(WALL)
            else:
                vw.append(self.board[x + dx[i]][y + dy[i]])
        return vw

    def make_grid(self):
        for i in range(self.cols):
            x = BORDER + self.xunit * i
            for j in range(self.rows):
                y = BORDER + self.yunit * j
                if i > 0 and self.wall[(i, j)][2]:
                    w = self.can.create_line(x, y - 1, x, y + self.yunit + 1, width=self.wallwidth)
                if j > 0 and self.wall[(i, j)][1]:
                    w = self.can.create_line(x - 1, y, x + self.xunit + 1, y, width=self.wallwidth)
        self.can.create_rectangle(BORDER, BORDER, self.wid - BORDER, self.hgt - BORDER, width=1 + self.wallwidth)

    def cmdHandler(self, who):
        dx = [1, 0, -1, 0]
        dy = [0, -1, 0, 1]
        x = self.player[who].x
        y = self.player[who].y
        vw = self.getview(x, y)
        self.explorer[who].feedback(vw)
        cmd = self.explorer[who].action()
        if cmd[0] == 2:
            dir = cmd[1]
            x = self.player[who].x
            y = self.player[who].y
            if not self.wall[(x, y)][dir]:
                newx = x + dx[dir]
                newy = y + dy[dir]
                self.player[who].move(newx, newy)
                if (newx, newy) == self.target:
                    self.running = False
        elif cmd[0] == 1:
            pass
        else:
            print('whoops')

    def playgame(self):
        self.cmdHandler(self.turn)
        self.turn = (self.turn + 1) % NPLAYER
        if self.running:
            self.win.after(self.ticker.get(), self.playgame)

    def automate(self):
        if self.running:
            return
        self.running = True
        self.win.after(self.ticker.get(), self.playgame)

    def stop(self):
        self.running = False


if __name__ == '__main__':
    win = Tk()
    win.geometry("+500+50")
    game = Game(win, GAMEHGT, GAMEWID)
    win.mainloop()