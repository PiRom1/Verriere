"""
Backend matériel simulé : aucune dépendance Raspberry Pi.
Reproduit l'interface utilisée par le projet (on/off/value pour les relais,
temperature/humidity/exit pour les DHT22).
"""

import random

_devices = {}


class FakeRelais:
    def __init__(self, gpio):
        self.gpio = gpio
        self.value = 0

    def on(self):
        self.value = 1

    def off(self):
        self.value = 0

    def toggle(self):
        self.value = 0 if self.value else 1

    @property
    def is_active(self):
        return bool(self.value)


class FakeDHT:
    def __init__(self, gpio):
        self.gpio = gpio

    @property
    def temperature(self):
        return round(random.uniform(18.0, 30.0), 1)

    @property
    def humidity(self):
        return round(random.uniform(40.0, 80.0), 1)

    def exit(self):
        pass


def relais(gpio):
    if gpio not in _devices:
        _devices[gpio] = FakeRelais(gpio)
    return _devices[gpio]


def dht(gpio):
    if gpio not in _devices:
        _devices[gpio] = FakeDHT(gpio)
    return _devices[gpio]
