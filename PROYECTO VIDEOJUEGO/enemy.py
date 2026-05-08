class Enemy:
    def __init__(self):
        self.name = "Eco Salvaje"
        self.hp = 50
        self.attack = 8

    def is_alive(self):
        return self.hp > 0