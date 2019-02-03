class Piece():

    def __init__(self, colour,position,power,name):
        self.colour=colour
        self.position=position
        self.power=power
        self.name=name

    def move(self,newPosition):
        raise notimplementederror

    def vaildMove(self,newPosition):
        raise notimplementederror

    def __str__(self,powerLevel=False):
        if powerLevel:
            return str(self.power)
        else:
            if self.colour=="white":
                return self.name.upper()
            else:
                return self.name.lower()
