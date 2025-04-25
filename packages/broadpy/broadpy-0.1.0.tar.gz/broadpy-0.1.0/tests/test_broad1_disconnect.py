# -*- coding:utf-8 -*-
"""
pytest for BRoaD1 Class (disconnected).
"""

import pytest
from sitcpy.rbcp import RbcpError

from src.broadpy.broad_base import BRoaDErrorCommunication


def test_start_read_disconnect(broad1_disconnect):
    with pytest.raises((BRoaDErrorCommunication, RbcpError)):
        broad1_disconnect.start_read(0)


def test_stop_read_disconnect(broad1_disconnect):
    with pytest.raises((BRoaDErrorCommunication, RbcpError)):
        broad1_disconnect.stop_read(0)
