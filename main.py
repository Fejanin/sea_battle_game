from random import randint

class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._length = length # длина корабля (число палуб)
        self._x = x # координаты корабля (целые значения в диапазоне [0; size), где size - размер игрового поля)
        self._y = y # координаты корабля (целые значения в диапазоне [0; size), где size - размер игрового поля)
        self._tp = tp # ориентация корабля; (1 - горизонтальная; 2 - вертикальная)
        self._is_move = True # возможно ли перемещение корабля (изначально равно True)
        self._cells = [1 for i in range(self._length)] # изначально список длиной length, состоящий из единиц (например, при length=3, _cells = [1, 1, 1]).
        # Список _cells будет сигнализировать о попадании соперником в какую-либо палубу корабля. Если стоит 1, то попадания 
        # не было, а если стоит значение 2, то произошло попадание в соответствующую палубу.

    def set_start_coords(self, x, y):
        # установка начальных координат (запись значений в локальные атрибуты _x, _y)
        self._x = x
        self._y = y

    def get_start_coords(self):
        # получение начальных координат корабля в виде кортежа x, y
        return self._x, self._y

    def move(self, go):
        # перемещение корабля в направлении его ориентации на go клеток (go = 1 - движение в одну сторону на клетку;
        # go = -1 - движение в другую сторону на одну клетку); движение возможно только если флаг _is_move = True
        if self._tp == 1:
            self._x += go
        else:
            self._y += go

    def is_collide(self, ship):
        # проверка на столкновение с другим кораблем ship (столкновением считается, если другой корабль или 
        # пересекается с текущим или просто соприкасается, в том числе и по диагонали); метод возвращает True, если столкновение 
        # есть и False - в противном случае;
        for i in self.get_all_coords():
            test_coords = []
            for j in ship.get_all_coords():
                test_coords += [j, (j[0], j[1] + 1), (j[0], j[1] - 1), (j[0] + 1, j[1]), (j[0] - 1, j[1]),
                                (j[0] + 1, j[1] + 1), (j[0] - 1, j[1] - 1), (j[0] + 1, j[1] - 1), (j[0] - 1, j[1] + 1)]
            if i in test_coords:
                return True
        return False

    def is_out_pole(self, size):
        # проверка на выход корабля за пределы игрового поля (size - размер игрового поля, обычно, size = 10); 
        # возвращается булево значение True, если корабль вышел из игрового поля и False - в противном случае
        if self._x < 1 or self._y < 1:
            return True
        if self._tp == 1:
            if self._x + self._length - 1 > size:
                return True
        else:
            if self._y + self._length - 1 > size:
                return True
        return False

    def __getitem__(self, ind):
        # С помощью магических методов __getitem__() и __setitem__() обеспечить доступ к коллекции _cells следующим образом:
        # value = ship[indx] # считывание значения из _cells по индексу indx (индекс отсчитывается от 0)
        # ship[indx] = value # запись нового значения в коллекцию _cells
        return self._cells[ind]

    def __setitem__(self, ind, value):
        self._cells[ind] = value

    def get_all_coords(self):
        if self._x and self._y:
            if self._tp == 1:
                return [(self._x + i, self._y) for i in range(self._length)]
            else:
                return [(self._x, self._y + i) for i in range(self._length)]


class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []
        self.pole = [['0' for _ in range(self._size)] for _ in range(self._size)]

    def init(self):
        # однопалубных - 4; двухпалубных - 3; трехпалубных - 2; четырехпалубный - 1 (ориентация этих кораблей должна быть случайной)
        # Корабли формируются в коллекции _ships следующим образом: однопалубных - 4; двухпалубных - 3; трехпалубных - 2; 
        # четырехпалубный - 1. Ориентация этих кораблей должна быть случайной. Для этого можно воспользоваться функцией randint 
        # следующим образом:
        # [Ship(4, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), Ship(3, tp=randint(1, 2)), ...]
        # Начальные координаты x, y не расставленных кораблей равны None.
        # После этого, выполняется их расстановка на игровом поле со случайными координатами так, чтобы корабли не пересекались 
        # между собой.
        self.pole = [['0' for _ in range(self._size)] for _ in range(self._size)]
        self._ships = [Ship(4, tp=randint(1, 2)),
                        Ship(3, tp=randint(1, 2)),
                        Ship(3, tp=randint(1, 2)),
                        Ship(2, tp=randint(1, 2)),
                        Ship(2, tp=randint(1, 2)),
                        Ship(2, tp=randint(1, 2)),
                        Ship(1, tp=randint(1, 2)),
                        Ship(1, tp=randint(1, 2)),
                        Ship(1, tp=randint(1, 2)),
                        Ship(1, tp=randint(1, 2))]
        self.arrange_ships()

    def arrange_ships(self):
        for ind in range(len(self._ships)):
            if ind == 0:
                while True:
                    x = randint(1, self._size)
                    y = randint(1, self._size)
                    self._ships[ind].set_start_coords(x, y)
                    if self._ships[ind].is_out_pole(self._size):
                        continue
                    break
            else:
                while True:
                    # break
                    x = randint(1, self._size)
                    y = randint(1, self._size)
                    self._ships[ind].set_start_coords(x, y)
                    if self._ships[ind].is_out_pole(self._size):
                        continue
                    for j in range(ind):
                        if self._ships[ind].is_collide(self._ships[j]):
                            break
                    else:
                        break
                    
                    

    def get_ships(self):
        # возвращает коллекцию _ships
        return self._ships

    def move_ships(self):
        # перемещает каждый корабль из коллекции _ships на одну клетку (случайным образом вперед или назад) в 
        # направлении ориентации корабля; если перемещение в выбранную сторону невозможно (другой корабль или пределы игрового поля), 
        # то попытаться переместиться в противоположную сторону, иначе (если перемещения невозможны), оставаться на месте
        pass

    def show(self):
        # отображение игрового поля в консоли (корабли должны отображаться значениями из коллекции _cells каждого корабля, 
        # вода - значением 0)
        # TODO расставить корабли
        for ship in self._ships:
            x, y = ship.get_start_coords()
            if x and y:
                if ship._tp == 1:
                    for i in range(len(ship._cells)):
                        self.pole[y - 1][x - 1 + i] = ship._cells[i]
                else:
                    for i in range(len(ship._cells)):
                        self.pole[y - 1 + i][x - 1] = ship._cells[i]
        for i in self.pole:
            print(*i, sep='')

    def get_pole(self):
        # получение текущего игрового поля в виде двумерного (вложенного) кортежа размерами size x size элементов
        pass



gp = GamePole()
gp.init()
print('-' * 50)
gp.show()
print('-' * 50)

'''
Пример отображения игрового поля:

0 0 1 0 1 1 1 0 0 0
1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 1
0 0 0 0 1 0 1 0 0 1
0 0 0 0 0 0 1 0 0 0
1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 1 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0
'''



'''
# Пример использования классов (эти строчки в программе не писать):

SIZE_GAME_POLE = 10

pole = GamePole(SIZE_GAME_POLE)
pole.init()
pole.show()

pole.move_ships()
print()
pole.show()
'''

