# -*- coding:utf-8 -*-
"""
pytest for BRoaD3 Class (disconnected).
"""

import pytest
from sitcpy.rbcp import RbcpError

from src.broadpy.broad_base import BRoaDErrorCommunication


def test_start_read_disconnect(broad3_disconnect):
    with pytest.raises((BRoaDErrorCommunication, RbcpError)):
        broad3_disconnect.start_read(0)


def test_stop_read_disconnect(broad3_disconnect):
    with pytest.raises((BRoaDErrorCommunication, RbcpError)):
        broad3_disconnect.stop_read(0)


def test_user_control_disconnect(broad3_disconnect):
    with pytest.raises(RbcpError):
        broad3_disconnect.user_control(0, True)


def test_read_user_control_disconnect(broad3_disconnect):
    with pytest.raises(RbcpError):
        broad3_disconnect.read_user_control(0)
