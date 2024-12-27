import math
import os
from collections import namedtuple
from enum import Enum, StrEnum, auto
from signal import SIGUSR1
from time import sleep

from sense_hat import (ACTION_HELD, ACTION_PRESSED, ACTION_RELEASED,
                       InputEvent, SenseHat)


class DisplayState(StrEnum):
    TEMP = auto()
    PRESSURE = auto()
    HUMIDITY = auto()


state: DisplayState = DisplayState.TEMP


class Colours(Enum):
    R = 0
    G = 1
    B = 2


WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
CYAN = [0, 255, 255]
YELLOW = [255,255,0]
SCROLL_SPEED = 0.075
PROCESS_LOOP_DELAY_SEC = 0.5

Readings = namedtuple("Readings", ["temp", "humidity", "pressure"])
sense = SenseHat()


def reset_and_exit():
    sense.clear()
    os.kill(os.getpid(), SIGUSR1)

def clear():
    sense.clear()

def pushed_middle(event: InputEvent):
    if event.action == ACTION_HELD:
        reset_and_exit()
    elif event.action == ACTION_PRESSED:
        clear()


def pushed_up(event: InputEvent):
    if event.action != ACTION_RELEASED:
        global state
        state = DisplayState.TEMP


def pushed_left(event: InputEvent):
    if event.action != ACTION_RELEASED:
        global state
        state = DisplayState.HUMIDITY


def pushed_right(event: InputEvent):
    if event.action != ACTION_RELEASED:
        global state
        state = DisplayState.PRESSURE


def get_env_readings() -> Readings:
    temp = sense.temperature
    pressure = sense.pressure
    humidity = sense.humidity

    return Readings(temp=temp, pressure=pressure, humidity=humidity)


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


def display_readings(readings: Readings):
    if state == DisplayState.TEMP:
        temp = readings.temp
        colour = get_temperature_colour(temp)
        sense.show_message(
            f"{temp:.0f}C", scroll_speed=SCROLL_SPEED, text_colour=colour
        )
    elif state == DisplayState.HUMIDITY:
        humidity = readings.humidity
        colour = get_humidity_colour(humidity)
        sense.show_message(
            f"{humidity:.0f}%", scroll_speed=SCROLL_SPEED, text_colour=colour
        )
    elif state == DisplayState.PRESSURE:
        pressure = readings.pressure
        colour = YELLOW
        sense.show_message(
            f"{pressure:.0f}mb", scroll_speed=SCROLL_SPEED, text_colour=colour
        )


def main() -> None:
    sense.stick.direction_middle = pushed_middle
    sense.stick.direction_up = pushed_up
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right

    while True:
        readings = get_env_readings()
        display_readings(readings)
        sleep(PROCESS_LOOP_DELAY_SEC)


if __name__ == "__main__":
    main()
