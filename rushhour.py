import sys
import heapq
from heuristics import *
from combo import Combo
from collections import deque
from vehicle import Vehicle
from NumCars import NumCars

GOAL_VEHICLE = Vehicle('X', 4, 2, 'H')

class PriorityQueue:
    '''A priority queue. Each item in the queue is associated with a priority. The queue gives efficient access to the minimum priority item.'''
    def __init__(self):
        self.__heap = []

    def push(self, item, priority):
        pair = (priority, item)
        heapq.heappush(self.__heap, pair)

    def pop(self):
        (priority, item) = heapq.heappop(self.__heap)
        return item, priority

    def isEmpty(self):
        return len(self.__heap) == 0
    
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
        for line in self.getBoard():
            s += '|{0}|\n'.format(''.join(line))
        s += '-' * 8 + '\n'
        return s

    def getBoard(self):
        board = [[' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' '],
                 [' ', ' ', ' ', ' ', ' ', ' ']]
        for vehicle in self.vehicles:
            x, y = vehicle.xPos, vehicle.yPos
            if vehicle.orientation == 'H':
                for i in range(vehicle.length):
                    board[y][x+i] = vehicle.name
            else:
                for i in range(vehicle.length):
                    board[y+i][x] = vehicle.name
        return board

    def solved(self):
        return GOAL_VEHICLE in self.vehicles

    def moves(self):
        gameBoard = self.getBoard()
        for v in self.vehicles:
            if v.orientation == 'H':
                if v.xPos - 1 >= 0 and gameBoard[v.yPos][v.xPos - 1] == ' ':
                    newVehicle = Vehicle(v.name, v.xPos - 1, v.yPos, v.orientation)
                    newVehicles = self.vehicles.copy()
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)
                if v.xPos + v.length <=5 and gameBoard[v.yPos][v.xPos + v.length] == ' ':
                    newVehicle = Vehicle(v.name, v.xPos + 1, v.yPos, v.orientation)
                    newVehicles = self.vehicles.copy()
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)
            else:
                if v.yPos -1 >= 0 and gameBoard[v.yPos - 1][v.xPos] == ' ':
                    newVehicle = Vehicle(v.name, v.xPos, v.yPos - 1, v.orientation)
                    newVehicles = self.vehicles.copy()
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)
                if v.yPos + v.length <= 5 and gameBoard[v.yPos + v.length][v.xPos] == ' ':
                    newVehicle = Vehicle(v.name, v.xPos, v.yPos + 1, v.orientation)
                    newVehicles = self.vehicles.copy()
                    newVehicles.remove(v)
                    newVehicles.add(newVehicle)
                    yield RushHour(newVehicles)

    
def loadFile(inFile):
        vehicles = []
        for line in inFile:
            line = line[:-1] if line.endswith('\n') else line
            id, x, y, orientation = line
            vehicles.append(Vehicle(id, int(x), int(y), orientation))
        return RushHour(set(vehicles))

def bfs(r, maxDepth=25):
        visited = set()
        solutions = list()
        depthStates = dict()

        queue = deque()
        queue.appendleft((r, tuple()))
        while len(queue) != 0:
            board, path = queue.pop()
            newPath = path + tuple([board])

            depthStates[len(newPath)] = depthStates.get(len(newPath), 0) + 1

            if len(newPath) >= maxDepth:
                break

            if board in visited:
                continue
            else:
                visited.add(board)

            if board.solved():
                solutions.append(newPath)
            else:
                queue.extendleft((move, newPath) for move in board.moves())
        return {'visited': visited,
                'solutions': solutions,
                'depthStates': depthStates}

def aStarSearch(r, maxDepth=25):
    visited = set()
    solutions = list()
    depthStates = dict()
    cost = 0
    nullH = NullHeuristic(r.getBoard())
    redH = RedDistHeuristic(r.getBoard())
    carsH = NumCars(r.getBoard())
    lingerH = LingeringCars(r.getBoard())
    comboH = Combo(r.getBoard())
    queue = PriorityQueue()
    queue.push((r, tuple(), cost), r.getBoard())
    while not queue.isEmpty():
        s, score = queue.pop()
        board = s[0]
        path = s[1]
        curCost = s[2]
        newPath = path + tuple([board])
        depthStates[len(newPath)] = depthStates.get(len(newPath), 0) + 1
        curCost += 1
        if s[0] in visited:
            continue
        else:
            visited.add(board)
        if s[0].solved():
            solutions.append(newPath)
            return {'visited': visited,
            'solutions': solutions,
            'depthStates': depthStates,
            'cost': curCost
            }
        else:
            successors = s[0].moves()
            for succ in successors:
                string_board = succ.getBoard()
                queue.push((succ, newPath, curCost),  lingerH.eval(string_board))
    return {'visited': visited,
            'solutions': solutions,
            'depthStates': depthStates,
            'cost': curCost
            }
    
def solutionSteps(solution):
        """Generate list of steps from a solution path."""
        steps = []
        for i in range(len(solution) - 1):
            r1, r2 = solution[i], solution[i+1]
            v1 = list(r1.vehicles - r2.vehicles)[0]
            v2 = list(r2.vehicles - r1.vehicles)[0]
            if v1.xPos < v2.xPos:
                steps.append('{0}R'.format(v1.name))
            elif v1.xPos > v2.xPos:
                steps.append('{0}L'.format(v1.name))
            elif v1.yPos < v2.yPos:
                steps.append('{0}D'.format(v1.name))
            elif v1.yPos > v2.yPos:
                steps.append('{0}U'.format(v1.name))
        return steps
        
if __name__ == '__main__':
        filename = sys.argv[1]
        with open(filename) as rushHourFile:
            rushhour = loadFile(rushHourFile)

        results =aStarSearch(rushhour, maxDepth=100)

        print("{0} Solutions found".format(len(results['solutions'])))
        for solution in results['solutions']:
            print( 'Solution: {0}'.format(', '.join(solutionSteps(solution))))
        print( '{0} Cost'.format(results['cost']))
        print( '{0} Nodes visited'.format(len(results['visited'])))