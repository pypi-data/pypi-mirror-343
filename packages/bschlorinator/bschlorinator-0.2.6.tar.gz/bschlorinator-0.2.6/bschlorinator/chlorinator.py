import asyncio
import datetime
import time

from serial import Serial
from collections.abc import Callable
from collections import defaultdict

import platform

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    if platform.machine().startswith("arm"):
        raise  # Fails if on Raspberry Pi
    else:
        from unittest.mock import MagicMock
        GPIO = None


from . import const


class SerialResponseParser:

    def __init__(self, response: list[bytes], multiplier, parser):
        self.response = response
        self.multiplier = multiplier
        self.parser = parser

    def parse(self):
        data = [value for value in map(ord, self.response)]
        return self.parser(data, self.multiplier)

    def __str__(self):
        return f"<SerialResponseParser response={self.response} multiplier={self.multiplier} parser={self.parser}>"

    def __repr__(self):
        return f"<SerialResponseParser response={self.response} multiplier={self.multiplier} parser={self.parser}>"

class BSChlorinator:
    def __init__(self, port: Serial, gpio_pin: int = 37, channel: int = 1):
        self.port = port
        self.gpio_pin = gpio_pin
        self._channel = channel
        self._sensor_data = defaultdict(str)
        self._loop_restarts = 0
        self._init_gpio()

    @property
    def channel(self) -> int:
        return self._channel

    @channel.setter
    def channel(self, value: int):
        self._channel = value - 1

    @property
    def loop_restarts(self) -> int:
        return self._loop_restarts

    @loop_restarts.setter
    def loop_restarts(self, value: int):
        self._loop_restarts = value

    @property
    def sensor_data(self) -> dict:
        return self._sensor_data

    def clear_buffer(self):
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()

    def _init_gpio(self):
        """Init GPIO"""
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial=GPIO.LOW)

    async def _configure_serial(self) -> None:
        """Configures serial port and channel to send on"""
        channel_cmd = f"ATS200={self.channel}"
        commands = [
            channel_cmd,
            "ATS201=1",
            "ATS202=7",
            "ATS250=2",
            "ATS252=1",
            "ATS255=0",
            "ATS256=2",
            "ATS258=1",
            "ATS296=1"
        ]
        self.clear_buffer()
        await asyncio.sleep(1)

        # Set serial to a command mode
        self.port.write(b"+++")
        await asyncio.sleep(1)

        for cmd in commands:
            print(f"Sending: {cmd}")
            self.port.write((cmd + "\x0d").encode())
            await asyncio.sleep(1)
        # Set serial back to data mode
        self.port.write(b'ATO\x0d')
        await asyncio.sleep(1)

    async def _reset_serial_module(self) -> None:
        """Reset serial module"""
        GPIO.output(self.gpio_pin, GPIO.LOW)
        await asyncio.sleep(3)
        GPIO.output(self.gpio_pin, GPIO.HIGH)
        await asyncio.sleep(1)

    async def _config_channel(self) -> None:
        """Configuration of channel for serial port"""
        channel_cmd = f'ATS200={self.channel}'
        self.clear_buffer()
        await asyncio.sleep(1)

        # Set serial to a command mode
        self.port.write(b'+++')
        await asyncio.sleep(1)
        self.port.write((channel_cmd + '\x0d').encode())
        await asyncio.sleep(1)
        # Get back to data mode
        self.port.write('ATO\x0d'.encode())
        await asyncio.sleep(1)

    def _read_line_cr(self, max_length: int = 256, timeout: float = 1.0) -> list[bytes]:
        """Reads bytes from a serial port and returns results as a list"""
        read_value = []
        self.port.timeout = timeout
        while len(read_value) < max_length:
            char = self.port.read(1)
            if not char:
                break
            read_value.append(char)
            # Breaks out if linebreak
            if char in (b'\r', b'\n'):
                break
        return read_value

    async def send_command(self, command: bytes):
        """Sends command to the serial port and returns response"""
        self.port.write(command)
        await asyncio.sleep(0.15)
        return self._read_line_cr()

    async def _update_sensor_data(self) -> None:
        """Reads and updates data of the chlorinator sensor"""
        # Clear buffer to prevent wrong values
        self.clear_buffer()
        zipped_sensors = zip(const.keys, const.commands, const.multipliers, const.parsers)
        for key, command, multiplier, parser in zipped_sensors:
            response = await self.send_command(command)
            print(f"Response: {response}")
            self._sensor_data[key] = SerialResponseParser(response, multiplier, parser).parse()
        # Update timestamp
        self._sensor_data['last_updated'] = time.strftime("%Y-%m-%d %H:%M:%S")

    async def sensor_loop(self):
        await self._reset_serial_module()
        print('bschlorinator reseted')
        await self._config_channel()
        print('bschlorinator channel configured')
        while True:
            print('entering sensor pool loop')
            try:
                async with asyncio.timeout(30):
                    await self._update_sensor_data()
            except asyncio.TimeoutError:
                print('sensor pool loop timeout exception occured')
                await self._reset_serial_module()
                await self._config_channel()
                self.loop_restarts += 1
            finally:
                await asyncio.sleep(10)



def read_line_cr(port: Serial, max_length: int = 256, timeout:float = 1.0) -> list[bytes]:
    """Reads bytes from serial port and returns results as list"""
    read_value = []
    port.timeout = timeout
    while len(read_value) < max_length:
        char = port.read(1)
        if not char:
            break
        read_value.append(char)
        # Breaks out if linebreak
        if char in (b'\r', b'\n'):
            break
    return read_value

async def send_command(port: Serial, command: bytes):
    """Sends command to the serial port and returns response"""
    port.write(command)
    await asyncio.sleep(0.15)
    return read_line_cr(port)


def parse_response(response: list[bytes], multiplier: float, parser: Callable):
    """Parses response to a string"""
    if response:
        data = [value for value in map(ord, response)]
        return parser(data, multiplier)
    return ''

async def read_sensor_data(port: Serial) -> dict:
    """Reads and updates data of chlorinator sensor"""
    # Clear buffer to prevent wrong values
    port.reset_input_buffer()
    port.reset_output_buffer()

    zipped_sensors = zip(const.keys, const.commands, const.multipliers, const.parsers)
    data = {}
    for key, command, multiplier, parser in zipped_sensors:
        print(f"Sending: {command}")
        response = await send_command(port, command)
        print(f"Response: {response}")
        data[key] = parse_response(response, multiplier, parser)
        print(f"Data: {data}")
    return data

async def configure_serial(port: Serial, channel: int = 1) -> None:
    """Configures serial port and channel to send on"""
    channel_cmd = f"ATS200={channel-1}"
    commands = [
        channel_cmd,
        "ATS201=1",
        "ATS202=7",
        "ATS250=2",
        "ATS252=1",
        "ATS255=0",
        "ATS256=2",
        "ATS258=1",
        "ATS296=1"
    ]
    port.reset_input_buffer()
    port.reset_output_buffer()
    await asyncio.sleep(1)

    # Set serial to a command mode
    port.write(b"+++")
    await asyncio.sleep(1)

    for cmd in commands:
        print(f"Sending: {cmd}")
        port.write((cmd + "\x0d").encode())
        await asyncio.sleep(1)
    # Set serial back to data mode
    port.write(b'ATO\x0d')
    await asyncio.sleep(1)


async def reset_serial_module(gpio_pin: int) -> None:
    """Reset serial module"""
    GPIO.output(gpio_pin, GPIO.LOW)
    await asyncio.sleep(3)
    GPIO.output(gpio_pin, GPIO.HIGH)
    await asyncio.sleep(1)

def init_gpio(gpio_pin: int) -> None:
    """Init GPIO"""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpio_pin, GPIO.OUT, initial=GPIO.LOW)

async def config_channel(port: Serial, channel: int) -> None:
    """Configuration of channel for serial port"""
    channel_cmd = f'ATS200={channel - 1}'
    port.reset_input_buffer()
    port.reset_output_buffer()
    await asyncio.sleep(1)

    # Set serial to a command mode
    port.write(b'+++')
    await asyncio.sleep(1)
    port.write((channel_cmd + '\x0d').encode())
    await asyncio.sleep(1)
    # Get back to data mode
    port.write('ATO\x0d'.encode())
    await asyncio.sleep(1)