mov = 0
mode = 2
class Explorer:

    def __init__(self, xstart, ystart, xgoal, ygoal):
        self.xgoal = xgoal
        self.ygoal = ygoal
        self.presentx = xstart
        self.presenty = ystart
        self.cord_visited = [[xstart, ystart]]
        self.cord_number_times = [1]
        self.xdir = 0 if self.xgoal - self.presentx > 0 else 2
        self.ydir = 3 if self.ygoal - self.presenty > 0 else 1

    def feedback(self, view):
        self.view = view

    def find_next_cord(self):
        x_cord = self.presentx
        y_cord = self.presenty
        global mov
        if mov[1] == 0:
            return [x_cord+1, y_cord]
        elif mov[1] == 1:
            return [x_cord, y_cord-1]
        elif mov[1] == 2:
            return [x_cord-1, y_cord]
        elif mov[1] == 3:
            return [x_cord, y_cord+1]


    def action(self):
        global mov, mode
        mov_ret = 0
        times = 999999
        if self.view[self.xdir] == 0:
            mov = [2, self.xdir]
            next_node = self.find_next_cord()
            if next_node in self.cord_visited:
                if [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0] < times:
                    times = [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0]
                    mov_ret = mov
                    mode = 0
            else:
                times = -2
                mov_ret = mov
                mode = 1
        if self.view[self.ydir] == 0:
            mov = [2, self.ydir]
            next_node = self.find_next_cord()
            if next_node in self.cord_visited:
                if [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0] < times:
                    times = [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0]
                    mov_ret = mov
            else:
                times = -2
                mov_ret = mov
        if self.view[self.xdir] == 0:
            mov = [2, (self.xdir+2) % 4]
            next_node = self.find_next_cord()
            if next_node in self.cord_visited:
                if [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0] < times:
                    times = [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0]
                    mov_ret = mov
            else:
                times = 0
                mov_ret = mov
        if self.view[self.xdir] == 0:
            mov = [2, (self.ydir+2) % 4]
            next_node = self.find_next_cord()
            if next_node in self.cord_visited:
                if [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0] < times:
                    times = [x for x in self.cord_number_times if self.cord_visited[x] == next_node][0]
                    mov_ret = mov
            else:
                times = 0
                mov_ret = mov
         #       self.cord_visited.append(next_node)
          #      self.cord_number_times.append(1)
        self.presentx = next_node[0]
        self.presenty = next_node[1]

        return mov_ret
