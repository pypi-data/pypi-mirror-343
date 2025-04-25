# -*- coding:utf-8 -*-
"""
concrete BRoaD class for BBT-020(BRoaD3).
"""

import sys

from sitcpy.rbcp import RbcpError

from .broad_base import LOGGER, BRoaD


class BRoaD3(BRoaD):
    """
    concrete BRoaD class for BBT-020(BRoaD3)
    Implements user control functions.
    """

    USER_CONTROL_NUM = 10
    MEASURE_COUNTER_PERIOD = 1

    def user_control(self, id_: int, on_off: bool) -> bool:
        """
        set the usercontrol signal.(IN-OPT:8, IN-USER:9)
        returns True for success.

        Args:
            id_ (int): User control number(0~9)
            on_off (bool): True:1, False:0

        Returns:
            bool: True(Write success)
        """

        if not 0 <= id_ < self.USER_CONTROL_NUM:
            raise ValueError(f"id_ ({id_}) must be 0~{self.USER_CONTROL_NUM -1}. ")
        try:
            # Get current UserControl register
            user_reg = self._rbcp.read(0x6E, 2)
            user_reg_int = int.from_bytes(user_reg, "big")
            mask = 0x1 << id_
            if on_off is True:
                # change bit to 1
                user_reg_int |= mask
            elif on_off is False:
                # change bit to 0
                inv_mask = ~mask
                user_reg_int &= inv_mask
            else:
                raise ValueError(f"on_off ({on_off}) must be boolen. ")
            # Write UserControl register
            user_reg = user_reg_int.to_bytes(2, "big")
            self._rbcp.write(0x6E, user_reg)
            return True
        except RbcpError as error:
            LOGGER.exception(error)
            raise

    def read_user_control(self, id_: int) -> bool:
        """
        read user control signal.(IN-OPT:8, IN-USER:9)

        Args:
            id_ (int): User control number(0~9)

        Returns:
            bool: True:1, False:0
        """
        if not 0 <= id_ < self.USER_CONTROL_NUM:
            raise ValueError(f"id_ ({id_}) must be 0~{self.USER_CONTROL_NUM -1}. ")
        try:
            # Get current UserControl register
            user_reg = self._rbcp.read(0x6E, 2)
            user_reg_int = int.from_bytes(user_reg, "big")
            mask = 0x1 << id_
            if user_reg_int & mask:
                return True
            return False
        except RbcpError as error:
            LOGGER.exception(error)
            raise


if __name__ == "__main__":
    if len(sys.argv) > 1:
        BROAD_TCP = 24
        BROAD_UDP = 4660
        ch = int(sys.argv[1])
        if len(sys.argv) > 2:
            broad_host = sys.argv[2]
        if len(sys.argv) > 3:
            BROAD_TCP = int(sys.argv[3])
        if len(sys.argv) > 4:
            BROAD_UDP = int(sys.argv[4])
        broad3 = BRoaD3(broad_host, BROAD_TCP, BROAD_UDP)
        broad3.connect()
        LOGGER.debug("version %s", broad3.version)
        signal = broad3.read_user_control(ch)
        LOGGER.debug("current usercontrol ch:%d %s" % (ch, signal))
        broad3.user_control(9, not signal)
        invert_signal = broad3.read_user_control(9)
        LOGGER.debug("current usercontrol (invert) ch:%d %s" % (ch, invert_signal))
        broad3.user_control(ch, signal)
        broad3.disconnect()
    else:
        print(
            "usage: broad <counter sec> [ip address=192.168.16.10] [tcp port=24] [udp_port=4660]"
        )
