# coding: utf-8

# very simple mixer using Libaudioverse.
# wraps a Simulation object
import queue
import threading
import struct
import nvwave
import config
import time


class Mixer(object):
    def __init__(self, sim, mix_ahead):
        self.sim = sim
        self.mix_ahead = mix_ahead
        self.queue = queue.Queue(mix_ahead + 1)
        self.player = nvwave.WavePlayer(
            channels=2,
            samplesPerSec=44100,
            bitsPerSample=16,
            outputDevice=config.conf["speech"]["outputDevice"],
            wantDucking=False,
        )
        self.feeding_thread = threading.Thread(target=self.feeder_func)
        self.playing_thread = threading.Thread(target=self.player_func)
        self.playing_thread.daemon = True
        self.feeding_thread.daemon = True
        self.playing_thread.start()
        self.feeding_thread.start()

    def feeder_func(self):
        while True:
            block = self.sim.get_block(2)
            max_sample = (1 << 15) - 1
            for i, j in enumerate(block):
                block[i] = j * max_sample
            struct_format = f"{len(block)}h"
            block_string = struct.pack(struct_format, *(int(i) for i in block))
            self.queue.put(block_string, block=True)

    def player_func(self):
        prev_device = config.conf["speech"]["outputDevice"]
        zero_string = struct.pack("882h", *[0] * 882)  # 10 ms of silence.
        while True:
            current_device = config.conf["speech"]["outputDevice"]
            if prev_device != current_device:
                self.player = nvwave.WavePlayer(
                    channels=2,
                    samplesPerSec=44100,
                    bitsPerSample=16,
                    outputDevice=config.conf["speech"]["outputDevice"],
                )
            prev_device = current_device
            try:
                send_string = self.queue.get(block=True, timeout=0.01)
                self.player.feed(send_string)
            except queue.Empty:
                self.player.feed(zero_string)
