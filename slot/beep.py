import pyaudio
import numpy as np

# 音声を出力するためのストリームを開く --- (*1)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                frames_per_buffer=1024,
                output=True)

# 適当なサイン波を生成する --- (*2)
samples = np.sin(np.arange(50000) / 20)

# サイン波を再生する --- (*3)
print("play")
stream.write(samples.astype(np.float32).tostring())
stream.close()