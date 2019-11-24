CAR_IDS = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
TRUCK_IDS = {'O', 'P', 'Q', 'R'}
"""
Code recycled from https://github.com/saschazar21/rushhour
Class responsible for the creation of a vehicle object, has fields
name, x, y, and orientation
"""
class Vehicle(object):
    def __init__(self, name, xPos, yPos, orientation):
        
        if name in CAR_IDS:
            self.name = name
            self.length = 2
        elif name in TRUCK_IDS:
            self.name = name
            self.length = 3
        else:
            raise ValueError('Invalid id {0}'.format(name))

        if 0 <= xPos <= 5:
            self.xPos = xPos
        else:
            raise ValueError('Invalid x {0}'.format(xPos))

        if 0 <= yPos <= 5:
            self.yPos = yPos
        else:
            raise ValueError('Invalid y {0}'.format(yPos))

        if orientation == "H":
            self.orientation = orientation
            xEnd = self.xPos + (self.length - 1)
            yEnd = self.yPos
        elif orientation == "V":
            self.orientation = orientation
            xEnd = self.xPos
            yEnd = self.yPos + (self.length - 1)
        else:
            raise ValueError('Invalid orientation {0}'.format(orientation))
            
        if xEnd > 5 or yEnd > 5:
            raise ValueError('Invalid configuration')
    
    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Vehicle({0}, {1}, {2}, {3})".format(self.name, self.xPos, self.yPos,
                                                    self.orientation)

    