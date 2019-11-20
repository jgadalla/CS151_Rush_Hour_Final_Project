import sys
from vehicle import Vehicle

GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')

class RushHour(object):

    def __init__(self, vehicles):
        self.vehicles = vehicles

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.vehicles == other.vehicles

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        s = '-' * 8 + '\n'
        for line in self.get_board():
            s += '|{0}|\n'.format(''.join(line))
        s += '-' * 8 + '\n'
        return s

    def get_board(self):
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            if vehicle.orientation == 'H':
                for i in range(vehicle.length):
                    board[y][x+i] = vehicle.id
            else:
                for i in range(vehicle.length):
                    board[y+i][x] = vehicle.id
        return board

    def load_file(in_file):
    vehicles = []
    for line in in_file:
        line = line[:-1] if line.endswith('\n') else line
        id, x, y, orientation = line
        vehicles.append(Vehicle(id, int(x), int(y), orientation))
    return RushHour(set(vehicles))

    def solved(self):
        return GOAL_VEHICLE in self.vehicles

    def moves(self):
        board = self.get_board()
        newVehicles = self.vehicles.copy()
        for v in self.vehicles:
            if v.orientation == 'H':
                if v.x - 1 >= 0 and board[v.y][v.x - 1] == ' ':
                    newVehicle = Vehicle(v.id, v.x - 1, v.y, v.orientation)
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)
                if v.x + v.length <=5 and board[v.y][v.x + v.length] == ' ':
                    newVehicle = Vehicle(v.id, v.x + 1, v.y, v.orientation)
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)
            else:
                if v.y -1 >= 0 and board[v.y - 1][v.x] == ' ':
                    newVehicle = Vehicle(v.id, v.x, v.y - 1, v.orientation)
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)
                if v.x + v.length <= 5 and board[v.y + v.length][v.x] == ' ':
                    newVehicle = Vehicle(v.id, v.x, v.y + 1, v.orientation)
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)

    def bfs(r, max_depth=25):
        visited = set()
        solutions = list()
        depth_states = dict()

        queue = deque()
        queue.appendleft((r, tuple()))
        while len(queue) != 0:
            board, path = queue.pop()
            new_path = path + tuple([board])

            depth_states[len(new_path)] = depth_states.get(len(new_path), 0) + 1

            if len(new_path) >= max_depth:
                break

            if board in visited:
                continue
            else:
                visited.add(board)

            if board.solved():
                solutions.append(new_path)
            else:
                queue.extendleft((move, new_path) for move in board.moves())

        return {'visited': visited,
                'solutions': solutions,
                'depth_states': depth_states}



    if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as rushhour_file:
        rushhour = load_file(rushhour_file)

    results = breadth_first_search(rushhour, max_depth=100)

    print '{0} Solutions found'.format(len(results['solutions']))
    for solution in results['solutions']:
        print 'Solution: {0}'.format(', '.join(solution_steps(solution)))

    print '{0} Nodes visited'.format(len(results['visited']))