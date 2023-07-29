class Handle:
    startingX = 0
    endingRight = 0
    endingLeft = 0
    thresh = 120
    def __init__(self, cx):
        self.startingX = cx
        self.endingRight = cx + self.thresh
        self.endingLeft = cx - self.thresh
    def checkSwipe(self, cx):
        if self.endingLeft < 0:
            return ['none', False]
        elif cx >= self.endingRight and cx > self.startingX:
            return ['right', True]
        elif cx <= self.endingLeft and cx < self.startingX:
            return ['left', True]
        else:
            return ['none', False]