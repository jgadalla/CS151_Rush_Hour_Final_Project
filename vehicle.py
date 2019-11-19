"""
Code recycled from https://github.com/saschazar21/rushhour
Class responsible for the creation of a vehicle object, has fields
id, x, y, and orientation
"""
class Vehicle(object):
    def __init__(self, id, x, y, orientation):
        
        self.id = id
        self.length = 2
        self.x = x
        self.y = y

        if orientation == "H":
            self.orientation = orientation
            x_end = self.x + (self.length - 1)
            y_end = self.y
        elif orientation == "V":
            self.orientation = orientation
            x_end = self.x
            y_end = self.y + (self.length - 1)
        
        if x_end > 5 or y_end > 5:
            raise ValueError('Invalid configuration')
    
    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Vehicle({0}, {1}, {2}, {3})".format(self.id, self.x, self.y,
                                                    self.orientation)

    