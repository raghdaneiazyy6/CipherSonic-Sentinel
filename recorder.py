# recorder.py
import sounddevice as sd
import wavio as wv

def record_audio(duration=5, filename="recording.wav"):
    try:
        fs = 44100
        recording = sd.rec(duration * fs, samplerate=fs, channels=1)
        sd.wait()
        wv.write(filename, recording, fs, sampwidth=2)
    except Exception as e:
        raise RuntimeError(f"Error recording audio: {e}")

if __name__ == "__main__":
  record_audio(duration=10, filename="recording.wav")
