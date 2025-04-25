# -*- coding:utf-8 -*-
"""
concrete BRoaD class for BBT-028(BRoaD1).
"""

import sys
import time

from .broad_base import LOGGER, BRoaD, sample_counter_function, sample_raw_function


class BRoaD1(BRoaD):
    """
    concrete BRoaD class for BBT-028(BRoaD1)
    """


if __name__ == "__main__":
    if len(sys.argv) > 1:
        BROAD_TCP = 24
        BROAD_UDP = 4660
        count_sec = int(sys.argv[1])
        if len(sys.argv) > 2:
            broad_host = sys.argv[2]
        if len(sys.argv) > 3:
            BROAD_TCP = int(sys.argv[3])
        if len(sys.argv) > 4:
            BROAD_UDP = int(sys.argv[4])
        broad = BRoaD1(broad_host, BROAD_TCP, BROAD_UDP)
        broad.connect()
        LOGGER.debug("version ]%s", broad.version)
        broad.set_raw_function(sample_raw_function)
        broad.set_counter_function(sample_counter_function)
        broad.connect_measure_counter()
        broad.start_read(0)
        time.sleep(count_sec)
        broad.stop_read(0)
        broad.disconnect_measure_counter()
        broad.disconnect()
    else:
        print(
            "usage: broad <counter sec> [ip address=192.168.16.10] [tcp port=24] [udp_port=4660]"
        )
