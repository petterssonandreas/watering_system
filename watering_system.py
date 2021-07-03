#!/usr/bin/env python

import os
import sys
from typing import Optional
from termcolor import colored
import argparse
from enum import Enum, auto, unique
import time

if os.name == 'nt':
    print(colored("NOTE: Running on windows, replacing RPi with fake lib!", "yellow"))
    # Replace libraries by fake ones
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi            # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake GPIO
    sys.modules['smbus'] = fake_rpi.smbus        # Fake smbus (I2C)

import RPi.GPIO as GPIO  # type: ignore

PUMP_PIN = 7

def init_gpio():
    """ Initialize GPIO pins """
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PUMP_PIN, GPIO.OUT)
    GPIO.output(PUMP_PIN, GPIO.LOW)

@unique
class PumpAction(Enum):
    ON = auto()
    OFF = auto()

def control_pump(action: PumpAction):
    """ Control pump """
    if action is PumpAction.ON:
        print("Turning pump ON")
        GPIO.output(PUMP_PIN, GPIO.HIGH)
    else:
        assert action is PumpAction.OFF
        print("Turning pump OFF")
        GPIO.output(PUMP_PIN, GPIO.LOW)


def main():
    """ Main function for watering system """
    parser = argparse.ArgumentParser(description="System for watering plants")

    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version 0.1")
    pump = parser.add_argument_group(title="Pump")
    pump_group = pump.add_mutually_exclusive_group()
    pump_group.add_argument("--on", action="store_const", dest="pump_action", default=None, const=PumpAction.ON, help="Turn pump on")
    pump_group.add_argument("--off", action="store_const", dest="pump_action", default=None, const=PumpAction.OFF, help="Turn pump off")

    args = parser.parse_args()
    print(args)

    init_gpio()
    if args.pump_action:
        control_pump(args.pump_action)

    return 0


if __name__ == "__main__":
    sys.exit(main())
