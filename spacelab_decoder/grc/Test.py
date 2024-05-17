#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: UDP to ZMQ Decoder
# GNU Radio version: 3.10.1.1

from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
from gnuradio import zeromq




class Test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "UDP to ZMQ Decoder", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.zmq_addr = zmq_addr = "tcp://127.0.0.1:2112"
        self.samp_rate = samp_rate = 48000
        self.baudrate = baudrate = 1200
        self.UDO_Port = UDO_Port = 2114

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, zmq_addr, 100, False, -1)
        self.network_udp_source_0 = network.udp_source(gr.sizeof_float, 1, UDO_Port, 0, 1472, True, False, False)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_rate/(baudrate), 0.001, 0, 0.25, 0.001)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()


        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.network_udp_source_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))


    def get_zmq_addr(self):
        return self.zmq_addr

    def set_zmq_addr(self, zmq_addr):
        self.zmq_addr = zmq_addr

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_rate/(self.baudrate))

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_rate/(self.baudrate))

    def get_UDO_Port(self):
        return self.UDO_Port

    def set_UDO_Port(self, UDO_Port):
        self.UDO_Port = UDO_Port




def main(top_block_cls=Test, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
