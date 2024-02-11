import pygame as pg
from entity import Entity


class Projectile(Entity):
    def __init__(self, position, dir=1) -> None:
        self.image = pg.Surface([20, 10])
        self.image.fill("red")
        self.dir = dir
        self.speed = 10

        if self.dir:
            self.moving_right = True
        else:
            self.moving_left = True

        super().__init__(self.image, position, 17, 9)

    def update(self, *args, **kwargs):
        super().set_speed(8)
        if self.dir and self.rect.x > 2000:
            self.kill()

        if not self.dir and self.rect.x < 0:
            self.kill()
        return super().update(*args, **kwargs)
