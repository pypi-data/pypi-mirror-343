# -*- coding:utf-8 -*-
"""
fixture definition for pytest.
"""

import time

import pytest

from src.broadpy import BRoaD1, BRoaD3

from .pseudo import PseudoBRoaD


@pytest.fixture()
def broad1():
    try:
        pseudo_broad = PseudoBRoaD()
        pseudo_broad.start()
        time.sleep(0.1)
        broad = BRoaD1("127.0.0.1", 24242, 4660)
        broad.connect()
        yield broad
    finally:
        broad.disconnect()
        pseudo_broad.stop()
        time.sleep(0.1)
        del pseudo_broad
        del broad


@pytest.fixture()
def broad1_disconnect():
    try:
        pseudo_broad = PseudoBRoaD()
        pseudo_broad.start()
        time.sleep(0.1)
        broad = BRoaD1("127.0.0.1", 24242, 4660)
        broad.connect()
        broad.connect_measure_counter()
        pseudo_broad.stop()
        yield broad
    finally:
        broad.disconnect()
        time.sleep(0.1)
        del pseudo_broad
        del broad


@pytest.fixture()
def broad3():
    try:
        pseudo_broad = PseudoBRoaD()
        pseudo_broad.start()
        time.sleep(0.1)
        broad = BRoaD3("127.0.0.1", 24242, 4660)
        broad.connect()
        yield broad
    finally:
        broad.disconnect()
        pseudo_broad.stop()
        time.sleep(0.1)
        del pseudo_broad
        del broad


@pytest.fixture()
def broad3_disconnect():
    try:
        pseudo_broad = PseudoBRoaD()
        pseudo_broad.start()
        time.sleep(0.1)
        broad = BRoaD3("127.0.0.1", 24242, 4660)
        broad.connect()
        broad.connect_measure_counter()
        pseudo_broad.stop()
        yield broad
    finally:
        broad.disconnect()
        time.sleep(0.1)
        del pseudo_broad
        del broad
