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

    def countrs(self):
        countrs = []
        for i in range(3):
            for j in range(self.size+2):
                if self.hor:
                    countrs.append(Dot(self.d.x+i-1, self.d.y+i-1))
                else:
                    countrs.append(Dot(self.d.x+i-1, self.d.y+i-1))
        return countrs

    def find_ship(self, d):
        if d in self.dots():
            return True
        return False


class Board:
    def __init__(self):
        # 2d list 6x6
        self.board = [['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', ''], ['', '', '', '', '', '']]
        for i in range(6):
            for j in range(6):
                self.board[i][j] = Dot(i, j)
        self.ships = []
        self.countrs = []
        self.ship_dots = []
        self.destr_ship_dots = []
        self.hiden = False

    def add_ship(self, sh: Ship):
        if sh.dots in self.board and sh.dots not in self.countrs:
            self.ships.append(sh)
            self.ship_dots += sh.dots()
            self.countrs += sh.countrs()

    def shoot(self, d: Dot):
        if d not in self.board:
            return 'out'
        if d in self.ship_dots:
            self.destr_ship_dots.append(self.ship_dots.pop(self.ship_dots.index(d)))
            for i in self.ships:
                if i.find_ship(d):
                    i.hp -= 1
                    if i.hp == 0:
                        self.ships.pop(i)

