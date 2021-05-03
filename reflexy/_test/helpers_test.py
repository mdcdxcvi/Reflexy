import os
import pygame
import pytest
from reflexy.helpers import (
    get_image_path,
    create_pygame_font,
    calc_acceleration,
)


def test_get_image_path():
    """Test the get_image_path function."""
    with pytest.raises(TypeError):
        get_image_path()


def test_create_pygame_font():
    """Assert the type of the font."""
    with pytest.raises(TypeError):
        create_pygame_font(name=0)

    with pytest.raises(TypeError):
        create_pygame_font(size="18")


def test_calc_acceleration():
    """Test acceleration functions."""
    with pytest.raises(TypeError):
        calc_acceleration(0, 0, 0, 0)

    with pytest.raises(TypeError):
        calc_acceleration(0, "0", 0, 0)

    with pytest.raises(TypeError):
        calc_acceleration(0, 0, "0", 0)

    with pytest.raises(TypeError):
        calc_acceleration(0, 0, 0, "0")

    with pytest.raises(ValueError):
        calc_acceleration("0", 1, 0, 1)
