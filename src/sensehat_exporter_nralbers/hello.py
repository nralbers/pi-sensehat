import math
import os
from enum import Enum
from signal import SIGUSR1, pause
from time import sleep

from sense_hat import (ACTION_HELD, ACTION_PRESSED, ACTION_RELEASED,
                       InputEvent, SenseHat)


class Colours(Enum):
    R = 0
    G = 1
    B = 2


WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]

sense = SenseHat()


def pushed_middle(event):
    if event.action != ACTION_RELEASED:
        sense.clear()
        os.kill(os.getpid(), SIGUSR1)


def fill_display(colour: list[int]):
    if len(colour) != 3:
        raise ValueError("RGB values require 3 ints")
    x = colour
    pixels = [x] * 64
    sense.set_pixels(pixels)


def get_gradient_function(start_rgb, end_rgb, min_val: float, max_val: float):
    def gradient_function(value):
        ratio = (value - min_val) / (max_val - min_val)
        colour = list()
        for col in Colours:
            col_val = (end_rgb[col.value] - start_rgb[col.value]) * ratio + start_rgb[
                col.value
            ]
            colour.append(math.floor(col_val))
        return colour

    return gradient_function


def get_temperature_colour(value):
    low_gradient = get_gradient_function(WHITE, BLUE, -20, 0)
    med_gradient = get_gradient_function(BLUE, GREEN, 0, 20)
    high_gradient = get_gradient_function(GREEN, RED, 20, 40)
    if value < -20:
        return WHITE
    elif value >= -20 and value < 0:
        return low_gradient(value)
    elif value >= 0 and value < 20:
        return med_gradient(value)
    elif value >= 20 and value < 40:
        return high_gradient(value)
    else:
        return RED


def get_humidity_colour(value):
    low_gradient = get_gradient_function(WHITE, BLUE, 0, 30)
    med_gradient = get_gradient_function(BLUE, GREEN, 30, 60)
    high_gradient = get_gradient_function(GREEN, RED, 60, 100)
    if value < 0:
        return WHITE
    elif value >= 0 and value < 30:
        return low_gradient(value)
    elif value >= 30 and value < 60:
        return med_gradient(value)
    elif value >= 60 and value < 100:
        return high_gradient(value)
    else:
        return RED


def tryout():
    while True:
        temp = sense.temperature
        sense.show_message(f"{temp:.0f} C", text_colour=get_temperature_colour(temp))
        sleep(0.5)
        humidity = sense.humidity
        sense.show_message(
            f"{humidity:.0f}%", text_colour=get_humidity_colour(humidity)
        )
        sleep(0.5)


# def orientation():
#     def pushed_middle(event):
#         if event.action != ACTION_RELEASED:
#             sense.clear()
#             os.kill(os.getpid(), SIGUSR1)

#     sense.stick.direction_middle = pushed_middle

#     while True:
#         orientation = sense.orientation
#         print(f"{orientation['pitch']}, r: {orientation['roll']}, y: {orientation['yaw']}")
#         sleep(0.5)

# def direction():
#     def pushed_middle(event):
#         if event.action != ACTION_RELEASED:
#             sense.clear()
#             os.kill(os.getpid(), SIGUSR1)

#     sense.stick.direction_middle = pushed_middle

#     while True:
#         direction = sense.compass
#         print(f"North={direction}")
#         sleep(0.5)


# def buttons():
#     x = 3
#     y = 3


#     def clamp(value, min_value=0, max_value=7):
#         return min(max_value, max(min_value, value))

#     def pushed_up(event: InputEvent):
#         global y
#         if event.action != ACTION_RELEASED:
#             y = clamp(y - 1)

#     def pushed_down(event):
#         global y
#         if event.action != ACTION_RELEASED:
#             y = clamp(y + 1)

#     def pushed_left(event):
#         global x
#         if event.action != ACTION_RELEASED:
#             x = clamp(x - 1)

#     def pushed_right(event):
#         global x
#         if event.action != ACTION_RELEASED:
#             x = clamp(x + 1)

#     def pushed_middle(event):
#         if event.action != ACTION_RELEASED:
#             sense.clear()
#             os.kill(os.getpid(), SIGUSR1)

#     def refresh():
#         sense.clear()
#         sense.set_pixel(x, y, 255, 255, 255)


#     sense.stick.direction_up = pushed_up
#     sense.stick.direction_down = pushed_down
#     sense.stick.direction_left = pushed_left
#     sense.stick.direction_right = pushed_right
#     sense.stick.direction_middle = pushed_middle
#     sense.stick.direction_any = refresh
#     refresh()
#     pause()

if __name__ == "__main__":
    sense.stick.direction_middle = pushed_middle
    tryout()
