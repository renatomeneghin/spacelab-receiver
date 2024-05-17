#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq

_DEFAULT_INPUT_FILE         = "/tmp/audio.wav"
_DEFAULT_SAMPLE_RATE_HZ     = 48000
_DEFAULT_BAUDRATE_BPS       = 1200
_DEFAULT_ZMQ_ADDRESS        = "tcp://127.0.0.1:2112"

class GMSK_Demod(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.zmq_address = zmq_address = "tcp://127.0.0.1:2112"
        self.sample_rate_port = sample_rate_port = 48000
        self.samp_rate = samp_rate = 1e6
        self.Baudrate_BPS = Baudrate_BPS = 1200

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, zmq_address, 100, False, (-1), True)
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_source_0.set_center_freq(0, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=(int(sample_rate_port/Baudrate_BPS)),
            gain_mu=0.25,
            mu=0,
            omega_relative_limit=0.001,
            freq_error=0,
            verbose=False,log=False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.digital_gmsk_demod_0, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_gmsk_demod_0, 0))


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
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_Baudrate_BPS(self):
        return self.Baudrate_BPS

    def set_Baudrate_BPS(self, Baudrate_BPS):
        self.Baudrate_BPS = Baudrate_BPS




def main(top_block_cls=GMSK_Demod, options=None):
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
