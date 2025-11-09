'''PLAYER MANAGEMENT SYSTEMS'''
class Player:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.inventory = []

    def attack_player(self, enemy):
        damage = self.attack - enemy.defense
        if damage > 0:
            enemy.health -= damage
            print(f"{self.name} attacks {enemy.name} for {damage} damage!")
            print(f"{enemy.name} has {enemy.health} health remaining.")
        else:
            print(f"{self.name} attacks {enemy.name} but it has no effect!")
            print(f"{enemy.name} has {enemy.health} health remaining.")
            enemy.attack_player(self)


class Enemy:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.health = 100
        self.attack = 10
        self.defense = 5

    def attack_player(self, player):
        damage = self.attack - player.defense
        if damage > 0:
            player.health -= damage
            print(f"{self.name} attacks {player.name} for {damage} damage!")
            print(f"{player.name} has {player.health} health remaining.")
        else:
            print(f"{self.name} attacks {player.name} but it has no effect!")
            print(f"{player.name} has {player.health} health remaining.")

class Relation:
    def __init__(self,playerid,gamerelation):
        self.playerid=playerid
        self.gamerelation=gamerelation

    def Relation(self,player,opponent):
        
