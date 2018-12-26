class Point:
    x = 0
    y = 0
    
    def __init__(self, px, py):
        self.x = px
        self.y = py
    
    def setx(self, px):
        self.x = px

    def sety(self, py):
        self.y = py

    def get(self):
        result = (self.x, self.y)
        return result

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

point = Point(3, 4)

print (point.get())

point.setx(5)
point.sety(10)

print (point.get())

point.move(10,23)

print (point.get())

