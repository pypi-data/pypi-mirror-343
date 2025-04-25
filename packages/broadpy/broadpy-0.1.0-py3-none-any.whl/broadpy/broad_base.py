# -*- coding:utf-8 -*-
"""
Abstract BRoaD class.
"""

import inspect
import select
import socket
import sys
import threading
import time
from typing import Optional

from sitcpy import rbcp
from sitcpy.rbcp import RbcpError

from .util.logger import setup_logger

LOGGER = setup_logger(__file__)


class BRoaDError(Exception):
    """
    Base Exception class
    """


class BRoaDErrorCommunication(BRoaDError):
    """
    Broad Communication Error
    """

    def __init__(self, ip, tcp_port, message):
        super().__init__(f"BRoaD {ip} :{tcp_port} Communication Error. {message}")


class BRoaD:
    """
    Abstract BRoaD class.
    Implements BRoaDI/ BRoaDIII common functions.
    """

    UDP_DEFAULT = 4660
    TCP_DEFAULT = 24
    TCP_BUFF_SIZE = 4096
    COUNTER_BYTES = 8  # bytes
    MEASURE_COUNTER_PERIOD = 5  # nsec
    MEASURE_COUNTER_NUM = 4

    def __init__(
        self, ip_addr: str, tcp_port: int = TCP_DEFAULT, udp_port: int = UDP_DEFAULT
    ):
        """
        constructor of BRoaD

        Args:
            ip_addr (str): BRoaD IP Address
            tcp_port (int, optional): BRoaD TCP port. Defaults to TCP_DEFAULT.
            udp_port (int, optional): BRoaD UDP. Defaults to UDP_DEFAULT.
        """
        self._if_param = {
            "ip_addr": ip_addr,
            "tcp_port": tcp_port,
            "udp_port": udp_port,
            "rbcp": None,
            "version": int(0).to_bytes(4, "big"),
        }
        self._socket = None
        self._rbcp = None
        self._counter_run = False  # flag to runing the worker thread.
        self._func_counter = None  # pass the counter no and value to the function
        self._func_raw = None  # pass the coutner raw bytes
        self._counter_thread = (
            None  # worker thread object for reading the measurement counters.
        )
        self._measure_counter_gate_mode = bytearray(self.MEASURE_COUNTER_NUM)

    def __del__(self):
        self.disconnect()

    @property
    def version(self) -> str:
        """
        Returns the version (4-byte hexadecimal string) obtained after
        connecting to the BRoaD main body.
        Returns "00000000" if not connected
        """
        return self._if_param["version"]

    @version.setter
    def version(self, read_version: bytes):
        """
        version read from BRoaD
        """
        self._if_param["version"] = read_version

    @property
    def ip_addr(self):
        """
        returns IP Adress of BRoaD
        """
        return self._if_param["ip_addr"]

    @property
    def tcp_port(self):
        """
        returns TCP port of BRoaD
        """
        return self._if_param["tcp_port"]

    @property
    def udp_port(self):
        """
        returns UDP port of BRoaD
        """
        return self._if_param["udp_port"]

    @property
    def _rbcp(self):
        """
        returns RBCP Interce of BRoaD
        """
        return self._if_param["rbcp"]

    @_rbcp.setter
    def _rbcp(self, connected_rbcp: Optional[rbcp.Rbcp]):
        """
        returns RBCP Interce of BRoaD

        Args:
            connected_rbcp (rbcp.Rbcp): connected_rbcp
        """
        self._if_param["rbcp"] = connected_rbcp

    def connect(self):
        """
        Connect to BRoaD.
        """
        self._rbcp = rbcp.Rbcp(self.ip_addr, self.udp_port)
        try:
            self.version = self._rbcp.read(0, 4)
        except rbcp.RbcpError:
            self._rbcp = None
            raise

    def disconnect(self):
        """
        disconnected from BRoaD.
        """
        self.disconnect_measure_counter()
        if self._rbcp:
            self._rbcp = None

    def set_counter_function(self, func_counter):
        """
        Set Measure counter callback function for Measure counter, counter_value.

        Args:
            func_counter (function): callback function for Measure counter Number, counter_value

        Raises:
            ValueError: not function
            ValueError: not 2 argument function
        """
        self._func_counter = None
        if not callable(func_counter):
            raise ValueError(f"{func_counter} is not callable")
        func_arg_count = len(inspect.signature(func_counter).parameters)
        if func_arg_count != 2:
            raise ValueError(
                f"{func_counter} arge num ({func_arg_count}) must be 2 (id_, counter)"
            )
        self._func_counter = func_counter

    def set_raw_function(self, func_raw):
        """
        Set Measure counter callback function for raw TCP data.

        Args:
            func_counter (function): callback function for raw TCP data

        Raises:
            ValueError: not function
            ValueError: not 1 argument function
        """
        self._func_raw = None
        if not callable(func_raw):
            raise ValueError(f"{func_raw} is not callable")
        func_arg_count = len(inspect.signature(func_raw).parameters)
        if func_arg_count != 1:
            raise ValueError(
                f"{func_raw} arge num ({func_arg_count}) must be 1 (counter_byte"
            )
        self._func_raw = func_raw

    def connect_measure_counter(self):
        """
        Connect measure counter TCP connection and read measure counter mode settings.

        Raises:
            BRoaDErrorCommunication: TCP connction failed.
        """
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(2.0)
            self._socket.connect((self.ip_addr, self.tcp_port))
            self._counter_run = True
            self._counter_thread = threading.Thread(target=self._counter_worker)
            self._counter_thread.start()
            self._read_measure_counter_mode()
        except Exception as e:
            self._socket = None
            self._counter_run = False
            raise BRoaDErrorCommunication(self.ip_addr, self.tcp_port, str(e))

    def disconnect_measure_counter(self):
        """
        Disconnect measure counter TCP connection
        """

        if self._counter_thread:
            self._counter_run = False
            self._counter_thread.join(5.0)

        if self._socket:
            self._socket.close()
        self._socket = None

        self._measure_counter_gate_mode = bytearray(self.MEASURE_COUNTER_NUM)

    def start_read(self, counter_num: int) -> bool:
        """
        Start Measure counter

        Args:
            counter_num (int): Measure counter number(0~3)

        Raises:
            ValueError: counter num is not in (0~3)
            BRoaDErrorCommunication: no tcp connection

        Returns:
            bool: True:Start success, False: This Measure counter is not User Control.
        """
        if not 0 <= counter_num < self.MEASURE_COUNTER_NUM:
            raise ValueError(
                f"counter num ({counter_num}) must be 0~{self.MEASURE_COUNTER_NUM -1}. "
            )
        if self._socket is None or self._counter_run is False:
            raise BRoaDErrorCommunication(
                self.ip_addr, self.tcp_port, "not tcp connection"
            )
        if self._is_measure_counter_control(counter_num):
            try:
                user_reg = 0x80.to_bytes(1, "big")
                self._rbcp.write(0x64 + counter_num, user_reg)
                return True
            except RbcpError as error:
                LOGGER.exception(error)
                raise
            except Exception as error:
                LOGGER.exception(error)
                raise
        return False

    def stop_read(self, counter_num: int) -> bool:
        """
        Stop Measure counter

        Args:
            counter_num (int): measure counter number(0~3)

        Raises:
            ValueError: counter num is not in (0~3)
            BRoaDErrorCommunication: no tcp connection

        Returns:
            bool: True:Stop success, False: This Measure counter is not User control.
        """
        if not 0 <= counter_num < self.MEASURE_COUNTER_NUM:
            raise ValueError(
                f"counter num ({counter_num}) must be 0~{self.MEASURE_COUNTER_NUM -1}. "
            )
        if self._socket is None or self._counter_run is False:
            raise BRoaDErrorCommunication(
                self.ip_addr, self.tcp_port, "not tcp connection"
            )
        if self._is_measure_counter_control(counter_num):
            try:
                user_reg = 0x00.to_bytes(1, "big")
                self._rbcp.write(0x64 + counter_num, user_reg)
                return True
            except RbcpError as error:
                LOGGER.exception(error)
                raise
            except Exception as error:
                LOGGER.exception(error)
                raise
        return False

    def _counter_worker(self):
        """
        measurement counter reading thread.
        This thread function starts and stops at connect_measure_counter and disconnect_measure_counter.
        """
        byte_array = bytearray()
        try:
            if self._socket is None:
                return
            while self._counter_run:
                readable, _, _ = select.select([self._socket], [], [], 0.05)
                if self._socket not in readable:
                    time.sleep(0)
                    continue
                received_data = self._socket.recv(self.TCP_BUFF_SIZE)
                if len(received_data) == 0:
                    self._socket.close()
                    self._socket = None
                    self._counter_run = False
                    LOGGER.exception(
                        f"BRoaD {self.ip_addr}:{self.tcp_port} Communication Error."
                    )
                    break
                byte_array += received_data
                if len(byte_array) >= self.COUNTER_BYTES:
                    while True:
                        raw_counter = byte_array[: self.COUNTER_BYTES]
                        byte_array = byte_array[self.COUNTER_BYTES :]
                        if self._func_raw:
                            self._func_raw(raw_counter)
                        if self._func_counter:
                            no_ = raw_counter[0] & 0x0F
                            value = int.from_bytes(raw_counter[4:], "big")
                            if self._is_measure_counter_nsec(no_):
                                value *= self.MEASURE_COUNTER_PERIOD
                            self._func_counter(no_, value)
                        elif self._func_raw is None:
                            LOGGER.debug("no counter function : %s", raw_counter.hex())
                        if len(byte_array) < self.COUNTER_BYTES:
                            break
        except Exception as system_error:
            LOGGER.exception("%s in counter_worker thread", system_error)
            if self._socket is not None:
                self._socket.close()
                self._socket = None
            self._counter_run = False
            return

    def _read_measure_counter_mode(self) -> bool:
        """
        Read measure counter mode settings

        Returns:
            bool: True
        """
        try:
            couter_mode_reg = self._rbcp.read(0x60, self.MEASURE_COUNTER_NUM)
            self._measure_counter_gate_mode = couter_mode_reg
            return True
        except RbcpError as error:
            LOGGER.exception(error)
            raise

    def _is_measure_counter_nsec(self, counter_num: int) -> bool:
        """
        Check measure counter SRC mode.

        0x00: Gate Time (nsec)
        0x01: True Time (nsec)
        0x10: Number of times that True appears (positive edge count)
        0x11: Number of times that State change (edge count)

        Args:
            counter_num (int): Measure Counter Number(0~3)

        Returns:
            bool: Measure counter mode is nsec
        """
        if 0 <= counter_num < self.MEASURE_COUNTER_NUM:
            mode = self._measure_counter_gate_mode[counter_num]
            src_value = (mode >> 2) & 0b0011
            return src_value in (0x00, 0x01)
        return False

    def _is_measure_counter_control(self, counter_num: int) -> bool:
        """
        Check measure counter GATE mode.

        0x00: User Conrol (You can control by read_start, read_stop)
        0x01: Measure During True
        0x10: Measure During Edge to Edge (only False to True)
        0x11: Measure During Edge to Edge (Both Edge)

        Args:
            counter_num (int): Measure Counter Number(0~3)

        Returns:
            bool: Measure Counter Mode is User Control
        """
        if 0 <= counter_num < self.MEASURE_COUNTER_NUM:
            mode = self._measure_counter_gate_mode[counter_num]
            gate_value = (mode) & 0b0011
            return gate_value == 0x00
        return False


def sample_counter_function(id_, count):
    """
    this is sample counter function to use for argument of
    set_counter_function()

    Args:
        id_ (int): Measurement Counter Number(0~3)
        count (int): Measurement Counter Value(nsec or pulse count)
    """

    LOGGER.info("counter %u:%u", id_, count)


def sample_raw_function(counter_byte: bytes):
    """
    this is sample raw counter function to use for argument of
    set_counter_function()

    counter_byte[63:60]: 0x01
    counter_byte[59:56]: Measure Counter Number(0x0~0x3)
    counter_byte[55:48]: 0x00
    counter_byte[47:40]: 0x00
    counter_byte[39:32]: 0x00
    counter_byte[31:0]: Measure Counter Value

    Args:
        counter_byte (bytes): Measurement Counter raw TCP data
    """

    LOGGER.info("counter bytes : %s", counter_byte.hex())


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
        broad = BRoaD(broad_host, BROAD_TCP, BROAD_UDP)
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
