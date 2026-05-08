class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

    def update(self, player):
        self.offset_x = player.x
        self.offset_y = player.y