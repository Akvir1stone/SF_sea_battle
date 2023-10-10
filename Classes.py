class Field:
    def __init__(self):
        # 2D array 6x6 filled with 'O'
        self.field = [['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O'], ['O', 'O', 'O', 'O', 'O', 'O']]
        self.ship3count = 0
        self.ship2count = 0
        self.ship1count = 0

    def shoot_at_point(self, x, y):
        if self.field[x][y] == 'O':
            self.field[x][y] = 'T'
            return False
        elif self.field[x][y] == '#':
            self.field[x][y] = 'X'
            return True
        else:
            raise ValueError('Вы уже стреляли в эту точку')

    def get_ships_count(self, size):
        if size == 1:
            return self.ship1count
        elif size == 2:
            return self.ship2count
        elif size == 3:
            return self.ship3count
        else:
            raise ValueError('Таких кораблей не существует')

    @property
    def get_field(self):
        return self.field


class Ship:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.size = 0
        self.horizontal = True

    @property
    def place_x(self):
        return self.x

    @property.setter
    def place_x(self, x):
        if 0 < x < 7:
            self.x = x
        else:
            raise ValueError('Вы вышли за пределы игрового поля')

    @property
    def place_y(self):
        return self.y

    @property.setter
    def place_y(self, y):
        if 0 < y < 7:
            self.y = y
        else:
            raise ValueError('Вы вышли за пределы игрового поля')

    @property
    def ship_size(self):
        return self.size

    @property.setter
    def ship_size(self, size):
        if 0 < size < 4:
            self.size = size
        else:
            raise ValueError('Нельзя поставить корабль такого размера')

    @property
    def place_horizontal(self):
        return self.horizontal

    @property.setter
    def place_horizontal(self, horizontal: bool):
        self.horizontal = horizontal
