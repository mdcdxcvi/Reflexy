import os
import pygame
import math


def get_image_path(filename: str, folder: str = "../images") -> str:
    """Return the path of a image.

    Keyword arguments:
    filename -- name of image
    """
    if not filename:
        raise TypeError("Missing filename argument.")

    return os.path.abspath(os.path.join(os.path.dirname(__file__), folder, filename))


def create_pygame_font(
    name: str = "Comic Sans", size: int = 18, bold: bool = False
) -> pygame.font.Font:
    """Return a font.

    Keyword arguments:
    size -- size of the image (defalt 18)
    name -- name of the font (defalt "Comic Sans")
    bold -- bold of the font (defalt False)
    """
    if not isinstance(name, str):
        raise TypeError(f"Font name must be a string. Got {type(name)}.")
    if not isinstance(size, int):
        raise TypeError(f"Font size must be an integer. Got {type(size)}.")
    return pygame.font.SysFont(name, size, bold)


def calc_acceleration(
    func_acc: str, time: float, tracker: float, acceleration: float
) -> float:
    """Calculate the acceleration.

    Keyword arguments:
    func_acc -- acceleration function (defalt "lin")
    time -- duration of the acceleration
    tracker -- current time
    acceleration -- current acceleration
    """
    if not isinstance(func_acc, str):
        raise TypeError(
            f"Acceleration function must be a string. Options: 'log', 'lin' and 'exp'. Got {type(func_acc)}."
        )

    if not (
        (isinstance(time, float) or isinstance(time, int))
        and (isinstance(tracker, float) or isinstance(tracker, int))
        and (isinstance(acceleration, float) or isinstance(acceleration, int))
    ):
        raise TypeError(
            f"Acceleration values must be numbers. Got time:{type(time)}, tracker:{type(tracker)} and acceleration:{type(acceleration)}."
        )

    if func_acc not in ["log", "lin", "exp"]:
        raise ValueError(
            f"Acceleration functions: 'log', 'lin' and 'exp'. Got '{func_acc}'."
        )

    elif func_acc == "log":
        if not (time - tracker):
            return 0

        log = math.log10(1 / acceleration * (time - tracker))
        if log < 0:
            return 0

        return (log + 2) / 2

    elif func_acc == "lin":
        return 1 / acceleration * (time - tracker)

    elif func_acc == "exp":
        return 2 ** (1 / acceleration * (time - tracker)) - 1

    else:
        return 0
