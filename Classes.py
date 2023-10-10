class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    def __init__(self, size, d: Dot, hor: bool, hp):
        self.size = size
        self.d = d
        self.hor = hor
        self.hp = hp

    def dots(self):
        dots = []
        for i in range(self.size):
            if self.hor:
                dots.append(Dot(self.d.x+i, self.d.y))
            else:
                dots.append(Dot(self.d.x, self.d.y+i))
        return dots