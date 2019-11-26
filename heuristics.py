class RedDistHeuristic:
    def __init__(self,problem):
        pass

    def eval(self, state):
        foundTargetCar = False
        count = 0
        for x in state[2]:
            if x == "X":
                foundTargetCar = True
                continue
            if foundTargetCar:
                count += 1
        return count