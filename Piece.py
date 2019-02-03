class Piece():

    def __init__(self, colour,position,power,name):
        self.colour=colour
        self.position=position
        self.power=power
        self.name=name

    def move(self,newPosition,board):
        if vaildMove(self,newPosition,board):
            self.position=newPosition
            return True
        else:
            return False

    def vaildMove(self,newPosition,board):
        raise notimplementederror

    def __str__(self,powerLevel=False):
        if powerLevel:
            return str(self.power)
        else:
            if self.colour=="white":
                return self.name.upper()
            else:
                return self.name.lower()
