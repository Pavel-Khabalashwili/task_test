import random

class Hero:
    # Базовый класс, который не подлежит изменению
    # У каждого наследника будут атрибуты:
    # - Имя
    # - Здоровье
    # - Сила
    # - Жив ли объект
    # Каждый наследник будет уметь:
    # - Атаковать
    # - Получать урон
    # - Выбирать действие для выполнения
    # - Описывать своё состояние

    max_hp = 150
    start_power = 10

    def __init__(self, name):
        self.name = name
        self.__hp = self.max_hp
        self.__power = self.start_power
        self.__is_alive = True

    def get_hp(self):
        return self.__hp

    def set_hp(self, new_value):
        self.__hp = max(new_value, 0)

    def get_power(self):
        return self.__power

    def set_power(self, new_power):
        self.__power = new_power

    def is_alive(self):
        return self.__is_alive

    def take_damage(self, damage):
        self.set_hp(self.get_hp() - damage)
        print(f"{self.name} получил удар с силой {round(damage)}. Осталось здоровья: {round(self.get_hp())}")
        if self.get_hp() <= 0:
            self.__is_alive = False

    def make_a_move(self, friends, enemies):
        self.set_power(self.get_power() + 0.1)

    def __str__(self):
        return f'Name: {self.name} | HP: {self.get_hp()}'

class Healer(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.magic_power = self.get_power() * 3

    def attack(self, target):
        target.take_damage(self.get_power() / 2)

    def take_damage(self, damage):
        super().take_damage(damage * 1.2)

    def heal(self, target):
        target.set_hp(target.get_hp() + self.magic_power)

    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')
        target_of_heal = min(friends, key=lambda x: x.get_hp())
        if target_of_heal.get_hp() < 60:
            print(f"исцеляет {target_of_heal.name}")
            self.heal(target_of_heal)
        else:
            if enemies:
                print(f"атакует {enemies[0].name}")
                self.attack(enemies[0])
        print('\n')

class Tank(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.defense = 1
        self.shield_up = False

    def attack(self, target):
        target.take_damage(self.get_power() / 2)

    def take_damage(self, damage):
        super().take_damage(damage / self.defense)

    def raise_shield(self):
        if not self.shield_up:
            self.shield_up = True
            self.defense *= 2
            self.set_power(self.get_power() / 2)
            print(f'{self.name} поднимает щит!')

    def lower_shield(self):
        if self.shield_up:
            self.shield_up = False
            self.defense /= 2
            self.set_power(self.get_power() * 2)
            print(f'{self.name} опускает щит!')

    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')
        if not enemies:
            return
        if self.get_hp() > 70:
            if self.shield_up:
                self.lower_shield()
            print(f"атакует {enemies[0].name}")
            self.attack(enemies[0])
        else:
            if not self.shield_up:
                self.raise_shield()
            print(f'атакует из-за щита {enemies[0].name}')
            self.attack(enemies[0])
        print('\n')

class Attacker(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.power_multiply = 1

    def attack(self, target):
        target.take_damage(self.get_power() * self.power_multiply)
        self.power_down()

    def take_damage(self, damage):
        super().take_damage(damage * (self.power_multiply / 2))

    def power_up(self):
        self.power_multiply *= 2

    def power_down(self):
        self.power_multiply /= 2

    def make_a_move(self, friends, enemies):
        print(self.name, end=' ')
        if self.power_multiply < 2:
            print('Усиливаемся!')
            self.power_up()
        else:
            target_of_attack = min(enemies, key=lambda x: x.get_hp(), default=None)
            if target_of_attack:
                print(f'атакует {target_of_attack.name}')
                self.attack(target_of_attack)
            else:
                print('Нет подходящей цели для атаки. Восстанавливает силы')
        super().make_a_move(friends, enemies)
        print('\n')
