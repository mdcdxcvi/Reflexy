import math


class SpiderBrain:
    def __init__(self):
        pass

    def shot(self, enemy_angle, cooldown_ray, self_pos, enemy_pos):
        dist = math.dist(self_pos, enemy_pos)
        return enemy_angle

    def move(self, enemy_angle, cooldown_ray):
        return enemy_angle


class SpiderAi:
    def __init__(self):
        pass

    def fit(self):
        pass

    def update(self):
        pass


class PlayerAi:
    def __init__(self):
        pass

    def fit(self):
        pass

    def update(self):
        pass
