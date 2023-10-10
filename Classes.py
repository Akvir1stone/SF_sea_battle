class Field:
    def __init__(self):
        # 2D array 6x6 filled with 'O'
        self.field = [['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O']]

    def shoot_at_point(self, x, y):
        if self.field[x][y] == 'O':
            self.field[x][y] = 'T'
            return False
        elif self.field[x][y] == '#':
            self.field[x][y] = 'X'
            return True
        else:
            raise ValueError('Вы уже стреляли в эту точку')

    def check_place(self, x, y):
        if 0 > x > 5:
            return True
        if self.field[x][y] == 'O':
            return True
        return False

    def place_ship(self, x, y):
        self.field[x][y] = '#'

    @property
    def get_field(self):
        return self.field


class Ship:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.size = 0
        self.horizontal = True

    def create_ship(self, x, y, size, hor, p):
        if 0 >= x > 6:
            self.x = x
        else:
            raise ValueError('Параметр х за пределами игрового поля')
        if 0 >= y > 6:
            self.y = y
        else:
            raise ValueError('Параметр у за пределами игрового поля')
        if 0 > size > 4:
            self.size = size
        else:
            raise ValueError('Недопустимый размер корабля')
        self.horizontal = hor
        if hor:
            for i in range(x-1, x+1):
                for j in range(y-1, y + size):
                    if not p.check_place(i, j):
                        raise ValueError('Здесь нельзя постваить корабль')
        else:
            for i in range(x-1, x + size):
                for j in range(y-1, y + 1):
                    if not p.check_place(i, j):
                        raise ValueError('Здесь нельзя постваить корабль')

