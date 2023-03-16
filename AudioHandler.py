# -*- coding: utf-8 -*-
#
#   author: yadoon
#
# 音频收集转译
import os
import random
import time

import wave

from pyaudio import PyAudio, paInt16

CHUNK = 1024


class AudioHandle:

    def __init__(self, framerate=16000, num_samples=2000, channels=1, sampwidth=2, TIME=5, upload_path='./audio/',
                 limit_time=10):
        # 采样频率
        self.framerate = framerate
        self.num_samples = num_samples
        self.channels = channels
        self.sampwidth = sampwidth
        self.TIME = TIME
        self.upload_path = upload_path
        self.limit_time = limit_time
        if not os.path.exists(self.upload_path):  # 判断所在目录下是否有该文件名的文件夹
            os.mkdir(self.upload_path)  # 创建静态文件存储路径

    def save_wave_file(self, filename, data):
        """save the data to the wavfile"""

        wf = wave.open(self.upload_path + filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes(b"".join(data))
        wf.close()

    def persistence_record(self):
        """save the data to the hdd"""
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=1,
                         rate=self.framerate, input=True,
                         frames_per_buffer=self.num_samples)
        my_buf = []
        count = 0
        # 控制录音时间
        print("start collecting...")
        while count < self.TIME * 8:
            string_audio_data = stream.read(self.num_samples)
            my_buf.append(string_audio_data)
            count += 1
            print('.')
        filename = 'audio' + str(int(time.time())) + '.wav'
        self.save_wave_file(filename, my_buf)
        stream.close()
        print("collecting finished")
        return filename

    def play(self, filename):
        wf = wave.open(self.upload_path + filename, 'rb')
        p = PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
        data = wf.readframes(CHUNK)
        while data != b"":
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    ah = AudioHandle()
    file = ah.persistence_record()

    ah.play(file)
