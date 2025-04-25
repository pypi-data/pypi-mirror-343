# -*- coding:utf-8 -*-
"""
Pseudo BRoaD Device Class for pytest.
"""

from sitcpy.rbcp_server import (
    DataGenerator,
    PseudoDevice,
    RbcpCommandHandler,
    RbcpServer,
    VirtualRegister,
)

TEST_VERSION_REGISTER = [0x00, 0x01, 0x10, 0x11]
TEST_USERCONTROL_REGISTER = [0xFF, 0xF0]
TEST_MEASURECOUNTER_REGISTER = [0x00, 0x01, 0x02, 0x0C]
TEST_TCP_DATA = [0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01]


def sample_counter_function(id_, count):
    """
    this is sample counter function to use for argument of
    set_counter_function()
    """
    print("counter %u:%u", id_, count)


def sample_raw_function(counter_byte: bytes):
    """
    this is sample raw counter function to use for argument of
    set_counter_function()
    """
    print("counter bytes : %s", counter_byte.hex())


class PseudoBRoaD:
    """
    Pseudo BRoaD Device for tests.
    """

    def __init__(self, tcp_port=24242, udp_port=4660):
        pseudo_server = self._create_rbcp_server(udp_port)
        pseudo_data_generator = self._create_data_generetor()
        rbcp_command_handler = RbcpCommandHandler("pdev$ ")
        rbcp_command_handler.bind(pseudo_server, pseudo_data_generator)
        self.pdev = PseudoDevice(
            rbcp_command_handler, pseudo_data_generator, pseudo_server, 9090, tcp_port
        )

    def start(self):
        self.pdev.start()

    def stop(self):
        self.pdev.stop()

    def _create_data_generetor(self) -> DataGenerator:
        pseudo_data_generator = DataGenerator()
        pseudo_data_generator.create_data = self._create_pseudo_data

        return pseudo_data_generator

    def _create_pseudo_data(self, data_unit_count):
        data = bytearray()
        data.extend(TEST_TCP_DATA)
        return data

    def _create_rbcp_server(self, _udp_port=4660) -> RbcpServer:
        pseudo_server = RbcpServer(udp_port=_udp_port)
        pseudo_server.registers.append((VirtualRegister(4, 0x00000000)))  # Version
        pseudo_server.write_registers(0x00, TEST_VERSION_REGISTER)
        pseudo_server.registers.append((VirtualRegister(2, 0x0000006E)))  # User Control
        pseudo_server.write_registers(0x6E, TEST_USERCONTROL_REGISTER)
        pseudo_server.registers.append(
            (VirtualRegister(8, 0x00000060))
        )  # Measure Counter
        pseudo_server.write_registers(0x60, TEST_MEASURECOUNTER_REGISTER)

        return pseudo_server
