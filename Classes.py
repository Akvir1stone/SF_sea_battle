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


class ShootOutOfBoard(Exception):
    pass


class Ship:
    def __init__(self, size, d: Dot, hor: bool, hp):
        self.size = size
        self.d = d
        self.hor = hor
        self.hp = hp
        if hor and d.x > 6 - size:
            raise ShipCreationException('Здесь нельзя поставить корабль')
        elif not hor and d.y > 6 - size:
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
                    countrs.append(Dot(self.d.x + j - 1, self.d.y + i - 1))
                else:
                    countrs.append(Dot(self.d.x + i - 1, self.d.y + j - 1))
        return countrs

    def find_ship(self, d):
        if d in self.dots():
            return True
        return False


class Board:
    def __init__(self):
        self.board = []
        self.board_dots = []
        for i in range(6):
            self.board.append([])
            for j in range(6):
                self.board[i].append(Dot(i, j))
                self.board_dots.append(Dot(i, j))
        self.ships = []
        self.countrs = []
        # 3 arrays created for optimizing ship search in methods
        self.ship_dots = []
        self.destr_ship_dots = []
        self.miss = []
        self.hidden = False

    def add_ship(self, sh: Ship):
        ship_in = False
        for i in sh.dots():
            if i in self.board_dots and i not in self.countrs:
                ship_in = True
                self.ship_dots.append(i)
            else:
                raise ShipPlacementException('Здесь нельзя поставить корабль')
        if ship_in:
            self.ships.append(sh)
            self.countrs += sh.countrs()

    def shoot(self, d: Dot):
        if d in self.miss or d in self.destr_ship_dots:
            return 'shooted'
        if d not in self.board_dots:
            raise ShootOutOfBoard('Координаты выстрела за пределами игрового поля')
        if d in self.ship_dots:
            self.destr_ship_dots.append(self.ship_dots.pop(self.ship_dots.index(d)))
            for i in self.ships:
                if i.find_ship(d):
                    i.hp -= 1
                    if i.hp == 0:
                        for j in i.countrs():
                            if j not in self.miss and j not in i.dots():
                                self.miss.append(j)
                        self.ships.pop(self.ships.index(i))
                        if not self.ships:
                            return 'win'
                        return 'destr'
                    return 'hit'
        self.miss.append(d)
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
        while True:
            try:
                x = int(input('Введите номер строки, по которой хотите выстрелить ')) - 1
                y = int(input('Введите номер столбца, по которому хотите выстрелить ')) - 1
                return Dot(x, y)
            except ValueError:
                print('Введите корректное значение')


class Game:
    def __init__(self):
        self.board = Board()
        self.enemy = Board()
        self.enemy.hidden = True

    def ask_ship(self, size):
        while True:
            print(f'Корабль длинной в {size} клетки(у)')
            while True:
                try:
                    x = int(input('Введите номер строки ')) - 1
                    y = int(input('Введите номер столбца ')) - 1
                    if size != 1:
                        hor = bool(int(input(
                            'Введите 0 - если хотите, чтобы нос корабля был направлен вправо, или 1 - чтобы нос был направлен вниз ')))
                    else:
                        hor = True
                except ValueError:
                    print('Введите корректное значение')
                else:
                    break
            try:
                self.board.add_ship(Ship(size, Dot(x, y), hor, size))
            except ShipPlacementException as e:
                print(e)
                print('Попробуйте создать корабль заново')
            except ShipCreationException as e:
                print(e)
                print('Попробуйте создать корабль заново')
            else:
                break

    def ask_ship_ai(self, size):
        i = 0
        if size != 1:
            hor = bool(random.randint(0, 1))
        else:
            hor = True
        try:
            self.enemy.add_ship(Ship(size, AI.ask(), hor, size))
        except ShipPlacementException:
            return False
        except ShipCreationException:
            return False
        else:
            return True

    def set_board(self):
        print('Корабли расставляются следующим образом: сначала вы выбираете координаты точки,')
        print('на которой будет стоять корма (задняя часть) корабля, а затем выбираете куда будет')
        print('направлен нос корабля')
        print('Между кораблями должен быть промежуток - минимум 1 клетка')
        while True:
            try:
                self.draw_playground()
                self.ask_ship(3)
                self.draw_playground()
                for i in [1, 2]:
                    self.ask_ship(2)
                    self.draw_playground()
                for i in [1, 2, 3, 4]:
                    while True:
                        try:
                            if not int(
                                    input('Если не осталось места для кораблей, введите 0, или 1 чтобы продолжить ')):
                                raise BoardOverflow()
                        except ValueError:
                            print('Введите корректное значение')
                        else:
                            break
                    self.ask_ship(1)
                    self.draw_playground()
            except BoardOverflow:
                self.board.ships = []
                self.board.countrs = []
                self.board.ship_dots = []
                print('Попробуйте расставить корабли занаво')
            else:
                break

    def random_board(self):
        while True:
            right_board = True
            try:
                if not self.ask_ship_ai(3):
                    right_board = False
                for i in [1, 2]:
                    if not self.ask_ship_ai(2):
                        right_board = False
                for i in [1, 2, 3, 4]:
                    if not self.ask_ship_ai(1):
                        right_board = False
            except BoardOverflow:
                self.enemy.ships = []
                self.enemy.countrs = []
                self.enemy.ship_dots = []
            else:
                if right_board:
                    break
                else:
                    self.enemy.ships = []
                    self.enemy.countrs = []
                    self.enemy.ship_dots = []

    def game_loop(self):
        play = False
        end = False
        while True:
            while True:
                self.draw_playground()
                print('Ваш ход')
                while True:
                    try:
                        fb = self.enemy.shoot(User.ask())
                    except ShootOutOfBoard as e:
                        print(e)
                        print('Попробуйте снова')
                    else:
                        break
                if fb == 'win':
                    print('Вы победили')
                    play = self.exit_restart()
                    end = True
                    break
                elif fb == 'destr':
                    print('Вы уничтожили корабль')
                elif fb == 'hit':
                    print('Вы попали по кораблю')
                elif fb == 'shooted':
                    print('Вы уже стреляли по этой точке')
                elif fb == 'miss':
                    print('Вы промахнулись')
                    break
            if end:
                break
            while True:
                fb = self.board.shoot(AI.ask())
                if fb == 'win':
                    print('Вы проиграли')
                    play = self.exit_restart
                    end = True
                    break
                elif fb == 'destr':
                    print('Ваш корабль уничтожен')
                elif fb == 'hit':
                    print('По вашему кораблю попали')
                elif fb == 'shooted':
                    pass
                elif fb == 'miss':
                    break
            if end:
                break
        if play:
            ngame = Game()
            ngame.begin_tutor()

    def draw_playground(self):
        print('            Игрок                              Компьютер')
        for i in range(6):
            line = ''
            enemy_l = ''
            for j in range(6):
                line += f'| {self.board.draw_dot(Dot(i, j))} |'
                enemy_l += f'| {self.enemy.draw_dot(Dot(i, j))} |'
            print(line, f' <{i + 1}> ', enemy_l)
            if i != 5:
                print('------------------------------   |   ------------------------------')
        print('  ^    ^    ^    ^    ^    ^     X     ^    ^    ^    ^    ^    ^  ')
        print('  1    2    3    4    5    6           1    2    3    4    5    6 > Y')

    def begin_tutor(self):
        print('Добро пожаловать в игру "Морской бой"')
        print('Игровое поле выглядит следующим образом:')
        self.draw_playground()
        print('Слева ваше поле, справа поле вашего врага, на поле будут расставлены корабли')
        print('Игроки смогут по очереди стрелять по полю противника, если игрок попадает по кораблю,')
        print('он ходит повторно')
        print('Побеждает тот игрок, который первым уничтожит все корабли противника')
        print('Корабли на поле будут помечены символом "#", однако игрок не может видеть корабли противника')
        print('Символом "Х" будут помечены попадания и уничтоженные корабли')
        print('Символом "О" будут помечены пустые или неизвестные клетки')
        print('Символом "Т" будут помечены промахи и область вокруг уничтоженных кораблей')
        print('Нажмите Enter чтобы начать')
        input()
        print('Расставьте корабли')
        # self.set_board()
        print('Компьютер расставляет корабли')
        self.random_board()
        self.game_loop()

    @staticmethod
    def exit_restart():
        if int(input('Если вы хотите начать игру заново введите "1", если хотите закончить введите "0" ')):
            return True
        else:
            return False


game = Game()
game.begin_tutor()
