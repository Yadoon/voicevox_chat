# -*- coding: utf-8 -*-
#
#   author: yadoon
#
# 文字转音频播放（日语）
import io
import time
import wave

import json
import pyaudio
import requests

# 望子（清晰、平静的声音）
favorite_speaker = 11
likes = [50, 5]


class Voicevox:
    def __init__(self, host="127.0.0.1", port=50021):
        self.host = host
        self.port = port

    def speak(self, text=None, speaker=47):  # VOICEVOX:ナースロボ＿タイプＴ

        params = (
            ("text", text),  # 语句文本:str
            ("speaker", speaker)  # 声音类型:int
        )

        init_q = requests.post(
            f"http://{self.host}:{self.port}/audio_query",
            params=params
        )

        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(init_q.json())
        )

        # 打开文件
        audio = io.BytesIO(res.content)

        with wave.open(audio, 'rb') as f:
            # 处理音频
            p = pyaudio.PyAudio()

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            stream = p.open(format=p.get_format_from_width(width=f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True,
                            stream_callback=_callback)

            # Voice再生
            stream.start_stream()
            while stream.is_active():
                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()


def main():
    vv = Voicevox()
    for i in range(50):
        vv.speak(text='こんにちは', speaker=i)


if __name__ == "__main__":
    main()
