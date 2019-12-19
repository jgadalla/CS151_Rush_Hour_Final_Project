class NullHeuristic:
    def __init__(self,problem):
        pass

    def eval(self, state):
        return 0

class RedDistHeuristic:
    def __init__(self,problem):
        pass

    def eval(self, state):
        foundTargetCar = False
        count = 0
        for x in state[2]:
            if x == "X":
                foundTargetCar = True
            if foundTargetCar and x != "X":
                count += 1
        return count

class NumCars:
    def __init__(self,problem):
        pass

    def eval(self, state):
        count = 0
        foundTargetCar = False
        for x in state[2]:
            if x == "X":
                foundTargetCar = True
                continue
            if foundTargetCar and x != ' ':
                count += 1
        return count


class Combo:
    def __init__(self,problem):
        pass

    def eval(self, state):
        red = RedDistHeuristic(state)
        d = NumCars(state)
        dist = red.eval(state)
        numCar = d.eval(state)
        return dist + numCar


class LingeringCars:
    def __init__(self,problem):
        pass

    def eval(self, state):
        countOb = 0
        count = 0
        index = 0
        visited = {}
        for x in state[2]:
            if x != 'X' and x != ' ' :
                #count number of obstacle cars
                countOb += 1
                letter = x
                #case above
                if state[1][index] == letter and state[3][index] != letter:
                    #if not a truck and not empty
                    if state[0][index] != ' ' and state[0][index] != x:
                        #if the bottom is also blocked
                        if state[3][index] != ' ':
                            #check that we haven't seen the blocking cars yet
                            if state[0][index] not in visited and state[3][index] not in visited:
                                visited[state[0][index]] = 1
                                visited[state[3][index]] = 1
                                #add move for pair of blocking cars
                                count += 1
                #below case
                elif state[3][index] == letter and state[1][index] != letter:
                    #For case with car, check if something is in row 4
                    if state[4][index] != ' ':
                        #Check if truck or not
                        if state[4][index] != x:
                            #If not truck, check for above blocking car
                            if state[1][index] != ' ':
                                #check if both blocking cars have been visited or not
                                if state[1][index] not in visited and state[4][index] not in visited:
                                    visited[state[1][index]] = 1
                                    visited[state[4][index]] = 1
                                    #add move for pair of blocking cars
                                    count += 1
                        #case where below car is a truck
                        else:
                            #check for above  and below blocking car
                            if state[1][index] != ' ' and state[5][index] != ' ':
                                #check if both have not been visited
                                if state[1][index] not in visited and state[5][index] not in visited:
                                    visited[state[1][index]] = 1
                                    visited[state[5][index]] = 1
                                    #add move for pair of blocking cars
                                    count += 1
                #middle case
                else:
                    #If we have a truck in the middle, and there is a car blocking on both sides
                    if state[0][index] != ' ' and state[3][index] != ' ':
                        #check if both blocking cars haven't been visited
                        if state[0][index] not in visited and state[4][index] not in visited:
                            visited[state[0][index]] = 1
                            visited[state[4][index]] = 1
                            count += 1
            if(index == 6):
                break
            index += 1
        return count + countOb