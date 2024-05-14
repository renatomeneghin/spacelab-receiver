#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: Renato
# GNU Radio version: 3.10.9.2

from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import zeromq

_DEFAULT_INPUT_FILE         = "/test/ping_nrz_invertido.wav"
_DEFAULT_SAMPLE_RATE_HZ     = 48000
_DEFAULT_AUDIO_RATE_HZ      = 48000
_DEFAULT_BAUDRATE_BPS       = 1200
_DEFAULT_ZMQ_ADDRESS        = "tcp://127.0.0.1:2112"

class gmsk_Test(gr.top_block):

    def __init__(self, input_file=_DEFAULT_INPUT_FILE, samp_rate=_DEFAULT_SAMPLE_RATE_HZ, baudrate=_DEFAULT_BAUDRATE_BPS, zmq_adr=_DEFAULT_ZMQ_ADDRESS):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.zmq_address = zmq_address = "tcp://127.0.0.1:2112"
        self.sample_rate_port = sample_rate_port = 48000
        self.samp_rate = samp_rate = 48000
        self.Baudrate_BPS = Baudrate_BPS = 1200

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, zmq_address, 100, False, (-1), True)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=40,
            gain_mu=0.25,
            mu=0,
            omega_relative_limit=0.001,
            freq_error=0,
            verbose=False,log=False)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('F:\\Users\\Renato\\Documents\\UFSC\\SpaceLab-UFSC-GitHub\\spacelab-receiver\\tests\\ping_nrz_invertido.wav', True)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_0, 1))
        self.connect((self.digital_gmsk_demod_0, 0), (self.zeromq_push_sink_0, 0))

    def get_zmq_address(self):
        return self.zmq_address

    def set_zmq_address(self, zmq_address):
        self.zmq_address = zmq_address

    def get_sample_rate_port(self):
        return self.sample_rate_port

    def set_sample_rate_port(self, sample_rate_port):
        self.sample_rate_port = sample_rate_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_Baudrate_BPS(self):
        return self.Baudrate_BPS

    def set_Baudrate_BPS(self, Baudrate_BPS):
        self.Baudrate_BPS = Baudrate_BPS
