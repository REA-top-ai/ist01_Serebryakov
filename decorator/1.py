import functools
from random import randint
def is_alive(func):
    def wrappper(self, *args, **kwargs):
        if self.health <= 0:
            print(f"{self.name} мертв и не может действовать!")
            return None
        return func(self, *args, **kwargs)
    return wrappper
def log_action(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        print(f"[LOG] Начало действия: {func.__name__}")
        result = func(self, *args, **kwargs)
        print(f"[LOG] Действия завершено.")
        return result
    return wrapper
def holy_bonus(func):
    def wrapper(self, *args, **kwargs):
        old_h, old_m = self.health, self.mana
        self.health *= 2
        self.mana *= 1.5
        result = func(self, *args, **kwargs)
        self.health, self.mana = old_h, old_m
        return result
    return wrapper
def holy_posoh(func):
    def wrapper(self, *args, **kwargs):
        bonus = 0
        if self.hero_class == "волшебник":
            self.mana += 5     
        result = func(self, *args, **kwargs)
        if self.hero_class == "волшебник": 
            self.mana -= 5   
        return result
    return wrapper
def casino(func):
    def wrapper(self, *args, **kwargs):
        if randint(0, 1) == 0:
            print("Ставка не сыграла, действие отменено!")
            return None
        return func(self, *args, **kwargs)
    return wrapper
class Hero():
    def __init__(self, name, hero_class):
        self.name = name
        self.hero_class = hero_class
        self.spells_names = {}
        self.items = {}

        if self.hero_class == "воин":
            self.health = 200 #тараску купил
            self.mana = 20
        elif self.hero_class == "волшебник":
            self.health = 100
            self.mana = 90

        
    @is_alive
    @holy_bonus
    def attack(self, damage):
        print("Герой нанёс урон:", damage)
    @log_action
    def heal(self, amount):
        self.health += amount
    @is_alive
    @casino
    @holy_posoh
    def cast_spell(self, spell_name):
        self.mana -= self.spells_names[spell_name]["mana_cost"]
        self.health += self.spells_names[spell_name]["health_increase"]
        print(f"Герой использовал заклинание {spell_name} и нанес {self.spells_names[spell_name]['mag_damage']} магического урона.")
    
    def add_spell(self, spell_name, mag_damage, mana_cost, health_increase):
        self.spells_names[spell_name] = {
            "mag_damage": mag_damage,
            "mana_cost": mana_cost,
            "health_increase": health_increase
        }
    def add_item(self, item_name, health_bonus, mana_bonus):
        self.items[item_name] = {
            "health_bonus": health_bonus,
            "mana_bonus": mana_bonus
        }
    


    