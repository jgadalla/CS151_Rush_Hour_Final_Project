class LingeringCars:
    def __init__(self,problem):
        pass

    def eval(self, state):
        count = 0
        index = 0
        for x in state[2]:
            
            
            if x != 'X' and x != ' ' :
                letter = x
                if state[1][index] == letter:
                    if state[0][index] != ' ' and state[0][index] != x:
                        count += 1
                elif state[3][index] == letter:
                    if state[4][index] != ' ' and state[4][index] != x:
                        count += 1
                    else:
                        if state[5][index] != letter and state[5][index] != ' ':
                            count += 1
                else:
                    if state[1][index] != ' ' or state[3][index] != ' ':
                        count += 1
            if(index == 6):
                break
            index += 1
        return count