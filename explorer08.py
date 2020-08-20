from random import randrange
list_of_moves = []
back_tracked = False
mov = 0
adjacency = []


class Explorer:

    def __init__(self, xstart, ystart, xgoal, ygoal): # 0-right, 1-up, 2-left, 3-down
        #self.xstart = xstart # May use later if doing something when player returns to starting position
        #self.ystart = ystart # May use later if doing something when player returns to starting position
        self.xgoal = xgoal
        self.ygoal = ygoal
        self.presentx = xstart
        self.presenty = ystart
        self.view = 0
        self.graph = []  # node_number, [neighbours], [open_unvisited_sides], [x_coordinate, y_coordinate]
        self.node_number = 1
        self.xdir = 0 if self.xgoal - self.presentx > 0 else 2
        self.ydir = 3 if self.ygoal - self.presenty > 0 else 1
        # TODO: Update initial node in graph

    def feedback(self, view):
        self.view = view
        if len(self.graph) == 0:
            self.graph.append([0, [], [], [self.presentx, self.presenty]])

    def get_adjacency(self):
        global adjacency
        length = len(self.graph)
        adjacency = [[0 for x in range(length)] for y in range(length)]
        for nodes in range(length):
            for x in range(len(self.graph[nodes][1])):
                adjacency[nodes][self.graph[nodes][1][x]] = 1

    def djkistra(self, from_cord, to_cord):
        p = [0 for x in range(len(self.graph))]
        d = [0 for x in range(len(self.graph))]
        to_node = ''
        from_node = ''
        explore = [0 for x in range(len(self.graph))]
        for x in range(len(self.graph)):
            if self.graph[x][3] == from_cord:
                from_node = x
                break
        for x in range(len(self.graph)):
            if self.graph[x][3 == to_cord]:
                to_node = x
                break
        self.get_adjacency()



        #Algorithm

        index = ''
        explore[from_node] = 1
        for i in range(2, len(self.graph)):
            d[i] = adjacency[1][i]
            p[i] = 1
        for i in range(2, len(self.graph)):
            minimum = 9999999
            for j in range(2, len(self.graph)):
                if explore[j] == 0 and d[j] < minimum:
                    minimum = d[j]
                    index = j
            explore[index] = 1
            for j in range(2, len(self.graph)):
                if explore[j] == 0 and d[j] > d[index] + adjacency[index][j]:
                    d[j] = d[index] + adjacency[index][j]
                    p[j] = index
                    pass
        pass


    def find_exit_near_dest(self):
        dist = 99999999
        current_node = 0
        for i in range(len(self.graph)):
            if len(self.graph[i][2]) != 0:  # if self.graph[i][3] != 0:
                current_dist = abs(self.xgoal - self.graph[i][3][0]) + abs(self.xgoal - self.graph[i][3][1])
                if current_dist <= dist:
                    dist = current_dist
                    current_node = [self.graph[i][3][0], self.graph[i][3][1]]
        return current_node

    def node_exists(self, cord):
        for i in range(len(self.graph)):
            if self.graph[i][3] == cord:
                return True, i
        return False, False

    def addnode(self, open_paths, x_coordinate, y_coordinate):
        self.graph.append([self.node_number, [], [], [x_coordinate, y_coordinate]])
        self.graph[-2][2] = [x for x in range(4) if open_paths[x] == 0]
        self.node_number += 1
        if open_paths[0] == 0:
            check_x = self.presentx + 1
            truth_value, node = self.node_exists([check_x, self.presenty])
            if truth_value:
                self.graph[node][2].remove(2)
                self.graph[node][1].append(self.graph[-2][0])
                self.graph[-2][1].append(node)
        if open_paths[1] == 0:
            check_y = self.presenty - 1
            truth_value, node = self.node_exists([self.presentx, check_y])
            if truth_value:
                self.graph[node][2].remove(3)
                self.graph[node][1].append(self.graph[-2][0])
                self.graph[-2][1].append(node)
        if open_paths[2] == 0:
            check_x = self.presentx - 1
            truth_value, node = self.node_exists([check_x, self.presenty])
            if truth_value:
                self.graph[node][2].remove(0)
                self.graph[node][1].append(self.graph[-2][0])
                self.graph[-2][1].append(node)
        if open_paths[3] == 1:
            check_y = self.presenty + 1
            truth_value, node = self.node_exists([self.presentx, check_y])
            if truth_value:
                self.graph[node][2].remove(1)
                self.graph[node][1].append(self.graph[-2][0])
                self.graph[-2][1].append(node)

    def move_direct_goal(self, view):
        xy = randrange(2)
        if xy == 0:
            if view[self.xdir] == 0:
                return [2, self.xdir]
            elif view[self.ydir] == 0:
                return [2, self.ydir]
            else:
                return 0
        elif xy == 1:
            if view[self.ydir] == 0:
                return [2, self.ydir]
            elif view[self.xdir] == 0:
                return [2, self.xdir]
            else:
                return 0

    def update_current_position(self):
        if mov[1] == self.xdir:
            self.presentx += 1 if self.xdir == 0 else -1
        if mov[1] == self.ydir:
            self.presenty -= 1 if self.ydir == 1 else -1
        self.xdir = 0 if self.xgoal - self.presentx > 0 else 2
        self.ydir = 3 if self.ygoal - self.presenty > 0 else 1

    def action(self):
        global list_of_moves, back_tracked, mov
        mov = 0
        if back_tracked:
            back_tracked = False


        if len(list_of_moves) == 0:
            mov = self.move_direct_goal(self.view)

            if mov != 0:
                if mov[1] == 0:
                    next_node = [self.presentx + 1, self.presenty]
                elif mov[1] == 1:
                    next_node = [self.presentx, self.presenty - 1]
                elif mov[1] == 2:
                    next_node = [self.presentx - 1, self.presenty]
                elif mov[1] == 3:
                    next_node = [self.presentx, self.presenty + 1]

                if self.node_exists(next_node)[0]:
                    open_node = self.find_exit_near_dest()
                    if open_node != [self.presentx, self.presenty]:
                        actual_goal = [self.xgoal, self.ygoal]
                        self.xgoal, self.ygoal = open_node
                        list_of_moves = self.djkistra([self.presentx, self.presenty],
                                                 [self.xgoal, self.ygoal])  # move back to nearest (to the goal) exit
                        self.xgoal, self.ygoal = actual_goal
                else:
                    if mov[1] == 0:
                        self.addnode(self.view, self.presentx + 1, self.presenty)
                    elif mov[1] == 1:
                        self.addnode(self.view, self.presentx, self.presenty - 1)
                    elif mov[1] == 2:
                        self.addnode(self.view, self.presentx - 1, self.presenty)
                    elif mov[1] == 3:
                        self.addnode(self.view, self.presentx, self.presenty + 1)
                    self.update_current_position()
                    return mov
            else:
                back_tracked = True

        if len(list_of_moves) != 1:
            mov = [2, list_of_moves.pop(0)]
            self.update_current_position()
            return mov
        elif len(list_of_moves) == 1:
            back_tracked = True
            mov = [2, list_of_moves.pop(0)]
            self.update_current_position()
            return mov
