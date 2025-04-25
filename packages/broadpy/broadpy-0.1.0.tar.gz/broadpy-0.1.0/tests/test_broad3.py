# -*- coding:utf-8 -*-
"""
pytest for BRoaD3 Class.
"""

import time

import pytest
from sitcpy.rbcp import RbcpError

from src.broadpy.broad_base import BRoaDErrorCommunication

from .pseudo import TEST_MEASURECOUNTER_REGISTER, TEST_TCP_DATA, TEST_VERSION_REGISTER


def test_connect(broad3):
    broad3.disconnect()
    broad3.connect()
    assert broad3._rbcp is not None
    assert broad3.version == bytearray(TEST_VERSION_REGISTER)
    broad3.disconnect()
    with pytest.raises(RbcpError):
        broad3._if_param["ip_addr"] = "Invalid"
        broad3.connect()
    assert broad3._rbcp is None


def test_disconnect(broad3):
    broad3.disconnect()
    assert broad3._rbcp is None


def test_set_raw_function(broad3):
    def raw_function(counter_byte):
        return

    broad3.set_raw_function(raw_function)
    assert broad3._func_raw == raw_function

    def invalid_raw_function(counter_byte, dummy_arg):
        return

    with pytest.raises(ValueError):
        broad3.set_raw_function(invalid_raw_function)
    assert broad3._func_raw is None
    with pytest.raises(ValueError):
        broad3.set_raw_function("Not callable")
    assert broad3._func_raw is None


def test_set_counter_function(broad3):
    def counter_function(id_, count):
        return

    broad3.set_counter_function(counter_function)
    assert broad3._func_counter == counter_function

    def invalid_counter_function(id_, count, dummy_arg):
        return

    with pytest.raises(ValueError):
        broad3.set_counter_function(invalid_counter_function)
    assert broad3._func_counter is None
    with pytest.raises(ValueError):
        broad3.set_counter_function("Not callable")
    assert broad3._func_counter is None


def test_connect_measure_counter(broad3):
    broad3.connect_measure_counter()
    assert broad3._socket is not None
    assert broad3._counter_run is True
    assert broad3._counter_thread.is_alive() is True
    assert broad3._measure_counter_gate_mode == bytearray(TEST_MEASURECOUNTER_REGISTER)
    broad3.disconnect_measure_counter()
    with pytest.raises(Exception):
        broad3._if_param["ip_addr"] = "Invalid"
        broad3.connect_measure_counter()
    assert broad3._socket is None
    assert broad3._counter_run is False
    assert broad3._counter_thread.is_alive() is False
    assert broad3._measure_counter_gate_mode == bytearray([0, 0, 0, 0])


def test_disconnect_measure_counter(broad3):
    broad3.connect_measure_counter()
    broad3.disconnect_measure_counter()
    assert broad3._socket is None
    assert broad3._counter_run is False
    assert broad3._counter_thread.is_alive() is False
    assert broad3._measure_counter_gate_mode == bytearray([0, 0, 0, 0])


def test_start_read(broad3):
    with pytest.raises(BRoaDErrorCommunication):
        broad3.start_read(0)
    broad3.connect_measure_counter()
    assert broad3.start_read(0) is True
    assert broad3.start_read(1) is False
    assert broad3.start_read(2) is False
    assert broad3.start_read(3) is True
    with pytest.raises(ValueError):
        broad3.start_read(-1)
        broad3.start_read(4)
    broad3.disconnect()
    with pytest.raises(Exception):
        broad3.start_read(0)


def test_stop_read(broad3):
    with pytest.raises(BRoaDErrorCommunication):
        broad3.stop_read(0)
    broad3.connect_measure_counter()
    assert broad3.stop_read(0) is True
    assert broad3.stop_read(1) is False
    assert broad3.stop_read(2) is False
    assert broad3.stop_read(3) is True
    with pytest.raises(ValueError):
        broad3.stop_read(-1)
        broad3.stop_read(4)
    broad3.disconnect()
    with pytest.raises(Exception):
        broad3.stop_read(0)


def test_set_raw_function_execute(broad3):
    test_byte = bytes()

    def raw_function(counter_byte):
        nonlocal test_byte
        test_byte = counter_byte

    broad3.set_raw_function(raw_function)
    broad3.connect_measure_counter()
    time.sleep(0.5)
    assert test_byte == bytearray(TEST_TCP_DATA)
    broad3.disconnect_measure_counter()


def test_set_counter_function_execute(broad3):
    counter_number = -1
    counter_value = -1

    def counter_function(id_, count):
        nonlocal counter_number, counter_value
        counter_number = id_
        counter_value = count

    broad3.set_counter_function(counter_function)
    broad3.connect_measure_counter()
    time.sleep(0.5)
    assert counter_number == 0
    assert counter_value == 1
    broad3.disconnect_measure_counter()


def test_user_control(broad3):
    assert broad3.user_control(0, True) is True
    assert broad3.user_control(9, False) is True
    with pytest.raises(ValueError):
        broad3.user_control(-1, True)
    with pytest.raises(ValueError):
        broad3.user_control(10, True)
    with pytest.raises(ValueError):
        broad3.user_control(0, "a")
    broad3.disconnect()
    with pytest.raises(Exception):
        broad3.user_control(0, True)


def test_read_user_control(broad3):
    assert broad3.read_user_control(0) is False
    assert broad3.read_user_control(9) is True
    with pytest.raises(ValueError):
        broad3.read_user_control(-1)
    with pytest.raises(ValueError):
        broad3.read_user_control(10)
    broad3.disconnect()
    with pytest.raises(Exception):
        broad3.read_user_control(0)
