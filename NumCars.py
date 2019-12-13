class NumCars:
    def __init__(self,problem):
        pass

    def eval(self, state):
        count = 0
        for x in state[2]:
            if x != 'X' and x != ' ' :
                count+= 1
        return count