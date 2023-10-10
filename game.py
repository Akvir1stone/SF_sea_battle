from Classes import Field, Ship

p1 = Field()
p2 = Field()


def draw_fields(f1, f2):
    f1 = f1.get_field
    f2 = f2.get_field
    print('            Игрок                              Компьютер')
    for i in range(6):
        line = ''
        enemy_l = ''
        for j in range(6):
            line += f'| {f1[i][j]} |'
            if f2[i][j] == '#':
                enemy_l += '| O |'
            else:
                enemy_l += f'| {f2[i][j]} |'
        print(line, f' <{i+1}> ', enemy_l)
        if i != 5:
            print('------------------------------   |   ------------------------------')
    print('  ^    ^    ^    ^    ^    ^     X     ^    ^    ^    ^    ^    ^  ')
    print('  1    2    3    4    5    6           1    2    3    4    5    6 > Y')


draw_fields(p1, p2)
