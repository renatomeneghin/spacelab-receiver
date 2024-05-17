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
import threading

_DEFAULT_UDP_PORT           = 2114
_DEFAULT_SAMPLE_RATE_HZ     = 48000
_DEFAULT_BAUDRATE_BPS       = 1200
_DEFAULT_ZMQ_ADDRESS        = "tcp://127.0.0.1:2112"

class UDPtoZMQ(gr.top_block):

    def __init__(self,UDP_Port=_DEFAULT_UDP_PORT, samp_rate=_DEFAULT_SAMPLE_RATE_HZ, baudrate=_DEFAULT_BAUDRATE_BPS, zmq_addr=_DEFAULT_ZMQ_ADDRESS):
        gr.top_block.__init__(self, "UDP to ZMQ Decoder", catch_exceptions=True)

        self._lock = threading.RLock()

        ##################################################
        # Variables
        ##################################################
        self.zmq_addr = zmq_addr
        self.samp_rate = samp_rate
        self.baudrate = baudrate
        self.UDP_Port = UDP_Port

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, zmq_addr, 100, False, -1)
        self.network_udp_source_0 = network.udp_source(gr.sizeof_float, 1, UDP_Port, 0, 1472, True, False, False)
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
        with self._lock:
            self.zmq_addr = zmq_addr

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        with self._lock:
            self.samp_rate = samp_rate
            self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_rate/(self.baudrate))

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        with self._lock:
            self.baudrate = baudrate
            self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_rate/(self.baudrate))

    def get_UDP_Port(self):
        return self.UDP_Port

    def set_UDP_Port(self, UDP_Port):
        with self._lock:
            self.UDP_Port = UDP_Port
