# -*- coding:utf-8 -*-
"""
pytest for BRoaD1 Class.
"""

import time

import pytest
from sitcpy.rbcp import RbcpError

from src.broadpy.broad_base import BRoaDErrorCommunication

from .pseudo import TEST_MEASURECOUNTER_REGISTER, TEST_TCP_DATA, TEST_VERSION_REGISTER


def test_connect(broad1):
    broad1.disconnect()
    broad1.connect()
    assert broad1._rbcp is not None
    assert broad1.version == bytearray(TEST_VERSION_REGISTER)
    broad1.disconnect()
    with pytest.raises(RbcpError):
        broad1._if_param["ip_addr"] = "Invalid"
        broad1.connect()
    assert broad1._rbcp is None


def test_disconnect(broad1):
    broad1.disconnect()
    assert broad1._rbcp is None


def test_set_raw_function(broad1):
    def raw_function(counter_byte):
        return

    broad1.set_raw_function(raw_function)
    assert broad1._func_raw == raw_function

    def invalid_raw_function(counter_byte, dummy_arg):
        return

    with pytest.raises(ValueError):
        broad1.set_raw_function(invalid_raw_function)
    assert broad1._func_raw is None
    with pytest.raises(ValueError):
        broad1.set_raw_function("Not callable")
    assert broad1._func_raw is None


def test_set_counter_function(broad1):
    def counter_function(id_, count):
        return

    broad1.set_counter_function(counter_function)
    assert broad1._func_counter == counter_function

    def invalid_counter_function(id_, count, dummy_arg):
        return

    with pytest.raises(ValueError):
        broad1.set_counter_function(invalid_counter_function)
    assert broad1._func_counter is None
    with pytest.raises(ValueError):
        broad1.set_counter_function("Not callable")
    assert broad1._func_counter is None


def test_connect_measure_counter(broad1):
    broad1.connect_measure_counter()
    assert broad1._socket is not None
    assert broad1._counter_run is True
    assert broad1._counter_thread.is_alive() is True
    assert broad1._measure_counter_gate_mode == bytearray(TEST_MEASURECOUNTER_REGISTER)
    broad1.disconnect_measure_counter()
    with pytest.raises(Exception):
        broad1._if_param["ip_addr"] = "Invalid"
        broad1.connect_measure_counter()
    assert broad1._socket is None
    assert broad1._counter_run is False
    assert broad1._counter_thread.is_alive() is False
    assert broad1._measure_counter_gate_mode == bytearray([0, 0, 0, 0])


def test_disconnect_measure_counter(broad1):
    broad1.connect_measure_counter()
    broad1.disconnect_measure_counter()
    assert broad1._socket is None
    assert broad1._counter_run is False
    assert broad1._counter_thread.is_alive() is False
    assert broad1._measure_counter_gate_mode == bytearray([0, 0, 0, 0])


def test_start_read(broad1):
    with pytest.raises(BRoaDErrorCommunication):
        broad1.start_read(0)
    broad1.connect_measure_counter()
    assert broad1.start_read(0) is True
    assert broad1.start_read(1) is False
    assert broad1.start_read(2) is False
    assert broad1.start_read(3) is True
    with pytest.raises(ValueError):
        broad1.start_read(-1)
        broad1.start_read(4)
    broad1.disconnect()
    with pytest.raises(Exception):
        broad1.start_read(0)


def test_stop_read(broad1):
    with pytest.raises(BRoaDErrorCommunication):
        broad1.stop_read(0)
    broad1.connect_measure_counter()
    assert broad1.stop_read(0) is True
    assert broad1.stop_read(1) is False
    assert broad1.stop_read(2) is False
    assert broad1.stop_read(3) is True
    with pytest.raises(ValueError):
        broad1.stop_read(-1)
        broad1.stop_read(4)
    broad1.disconnect()
    with pytest.raises(Exception):
        broad1.stop_read(0)


def test_set_raw_function_execute(broad1):
    test_byte = bytes()

    def raw_function(counter_byte):
        nonlocal test_byte
        test_byte = counter_byte

    broad1.set_raw_function(raw_function)
    broad1.connect_measure_counter()
    time.sleep(0.5)
    assert test_byte == bytearray(TEST_TCP_DATA)
    broad1.disconnect_measure_counter()


def test_set_counter_function_execute(broad1):
    counter_number = -1
    counter_value = -1

    def counter_function(id_, count):
        nonlocal counter_number, counter_value
        counter_number = id_
        counter_value = count

    broad1.set_counter_function(counter_function)
    broad1.connect_measure_counter()
    time.sleep(0.5)
    assert counter_number == 0
    assert counter_value == 5
    broad1.disconnect_measure_counter()
