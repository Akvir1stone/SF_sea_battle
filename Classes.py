import random


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class ShipCreationException(Exception):
    pass


class ShipPlacementException(Exception):
    pass


class BoardOverflow(Exception):
    pass


class Ship:
    def __init__(self, size, d: Dot, hor: bool, hp):
        self.size = size
        self.d = d
        self.hor = hor
        self.hp = hp
        if hor and d.y > 6 - size:
            raise ShipCreationException('Здесь нельзя поставить корабль')
        elif not hor and d.x > 6 - size:
            raise ShipPlacementException('Здесь нельзя поставить корабль')

    def dots(self):
        dots = []
        for i in range(self.size):
            if self.hor:
                dots.append(Dot(self.d.x + i, self.d.y))
            else:
                dots.append(Dot(self.d.x, self.d.y + i))
        return dots

    def countrs(self):
        countrs = []
        for i in range(3):
            for j in range(self.size + 2):
                if self.hor:
                    countrs.append(Dot(self.d.x + i - 1, self.d.y + i - 1))
                else:
                    countrs.append(Dot(self.d.x + i - 1, self.d.y + i - 1))
        return countrs

    def find_ship(self, d):
        if d in self.dots():
            return True
        return False


class Board:
    def __init__(self):
        # 2d list 6x6
        self.board = []
        for i in range(6):
            self.board.append([])
            for j in range(6):
                self.board[i].append(Dot(i, j))
        self.ships = []
        self.countrs = []
        # 3 arrays created for optimizing ship search in methods
        self.ship_dots = []
        self.destr_ship_dots = []
        self.miss = []
        self.hidden = False

    def add_ship(self, sh: Ship):
        if sh.dots in self.board and sh.dots not in self.countrs:
            self.ships.append(sh)
            self.ship_dots += sh.dots()
            self.countrs += sh.countrs()
        else:
            del sh
            raise ValueError('Здесь нельзя поставить корабль')

    def shoot(self, d: Dot):
        if d not in self.board:
            return 'out'
        if d in self.ship_dots:
            self.destr_ship_dots.append(self.ship_dots.pop(self.ship_dots.index(d)))
            for i in self.ships:
                if i.find_ship(d):
                    i.hp -= 1
                    if i.hp == 0:
                        for j in i.countrs():
                            if j not in self.miss and j not in i.dots():
                                self.miss.append(j)
                        self.ships.pop(i)
                        if not self.ships:
                            return 'win'
                        return 'destr'
                    return 'hit'
        return 'miss'

    def draw_dot(self, d: Dot):
        if d in self.ship_dots and not self.hidden:
            return '#'
        if d in self.destr_ship_dots:
            return 'X'
        if d in self.miss:
            return 'T'
        return 'O'


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    @staticmethod
    def ask():
        return Dot()

    def turn(self):
        self.enemy.shoot(self.ask())


class AI(Player):
    @staticmethod
    def ask():
        x = random.randint(0, 5)
        y = random.randint(0, 5)
        return Dot(x, y)


class User(Player):
    @staticmethod
    def ask():
        x = int(input('Введите номер строки, по которой хотите выстрелить')) - 1
        y = int(input('Введите номер столбца, по которому хотите выстрелить')) - 1
        return Dot(x, y)


class Game:
    def __init__(self):
        self.board = Board()
        self.enemy = Board()

    def ask_ship(self, size):
        while True:
            print(f'Корабль длинной в {size} клетки(у)')
            x = int(input('Введите номер строки'))
            y = int(input('Введите номер столбца'))
            if size != 1:
                hor = bool(input(
                    'Введите 1 если хотите, чтобы нос корабля был направлен вправо, или 0, чтобы нос был направлен вниз'))
            else:
                hor = True
            try:
                self.board.add_ship(Ship(size, Dot(x, y), hor, size))
            except ShipPlacementException:
                print('Попробуйте создать корабль заново')
            except ShipCreationException:
                print('Попробуйте создать корабль заново')
            else:
                break

    def ask_ship_ai(self, size):
        i = 0
        while i < 2000:
            x = int(AI.ask())
            y = int(AI.ask())
            if size != 1:
                hor = bool(random.randint(0, 1))
            else:
                hor = True
            try:
                self.board.add_ship(Ship(size, Dot(x, y), hor, size))
            except ShipPlacementException:
                i += 1
            except ShipCreationException:
                i += 1
            else:
                break
        raise BoardOverflow()

    def set_board(self):
        print('Корабли расставляются следующим образом: сначала вы выбираете координаты точки,')
        print('на которой будет стоять корма (задняя часть) корабля, а затем выбираете куда будет')
        print('направлен нос корабля')
        while True:
            try:
                self.ask_ship(3)
                for i in [1, 2]:
                    self.ask_ship(2)
                for i in [1, 2, 3, 4]:
                    if not int(input('Если не осталось места для кораблей, введите 0, или 1 чтобы продолжить')):
                        raise BoardOverflow()
                    self.ask_ship(1)
            except BoardOverflow:
                self.board.ships = []
                self.board.countrs = []
                self.board.ship_dots = []
                print('Попробуйте расставить корабли занаво')
            else:
                break

    def random_board(self):
        while True:
            try:
                self.ask_ship_ai(3)
                for i in [1, 2]:
                    self.ask_ship_ai(2)
                for i in [1, 2, 3, 4]:
                    self.ask_ship_ai(1)
            except BoardOverflow:
                self.board.ships = []
                self.board.countrs = []
                self.board.ship_dots = []
            else:
                break

# Game() with methods: set_board, random_board, begin_tutor, game_loop, exit
