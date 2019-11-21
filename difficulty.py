import sys
import gameboard

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as rushHourFile:
        r = gameboard.loadFile(rushHourFile)

    results = gameboard.bfs(r, maxDepth=100)
    solutions = results['solutions']
    numSolutions = len(solutions)

    if numSolutions == 0:
        print('Impossible')
        sys.exit(1)

    solutions.sort(key=lambda x: len(x))
    shortestSolution = len(solutions[0])

    if shortestSolution < 20 or numSolutions > 200:
        print('Easy')
    elif shortestSolution > 50 or numSolutions < 20:
        print('Hard')
    else:
        print('Moderate')
