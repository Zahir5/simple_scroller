import os
import pygame as pg
GROUND_POS = 650

DISPLAY_WIDTH = 1920
DISPLAY_HEIGHT = 960
DIMS = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

project_dir = os.path.dirname(os.path.abspath(__file__))
img_dir = project_dir + "/assets/images"


def get_bg(level):
    image = pg.image.load(f"{img_dir}/levels/{level}.png")
    return pg.transform.scale(image, DIMS)


LEVELS = [
    {
        "bg": get_bg(1),
    },
    {
        "bg": get_bg(1),
        "enemy_img": pg.transform.flip(
            pg.image.load(img_dir+"/enemy_soldier.png"),
            flip_x=True,
            flip_y=False),
        "enemy_count": 2
    },
    {
        "bg": get_bg(2),
        "enemy_img": pg.transform.flip(
            pg.image.load(img_dir+"/enemy_soldier.png"),
            flip_x=True,
            flip_y=False),
        "enemy_count": 3
    },
    {
        "bg": get_bg(3),
        "enemy_img": pg.transform.flip(
            pg.image.load(img_dir+"/enemy_tank.png"),
            flip_x=True,
            flip_y=False),
        "enemy_count": 1
    },

]
