import wave
import pyaudio


def audio_recording(RATE,FRAMES_PER_BUFFER,CHANNELS,FORMAT):
    # create the pyaudio object
    p = pyaudio.PyAudio()

    # create a stream object
    stream = p.open(
        rate =RATE,
        frames_per_buffer=FRAMES_PER_BUFFER,
        format=FORMAT,
        channels=CHANNELS,
        input=True
    )
    print("Start Recording...🎤")
    seconds = 20
    frames = []

    for i in range(0,int(RATE/FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)
    print("Recording Ended 🔚")
    stream.stop_stream()
    stream.close()
    p.terminate()

    # open a file with the wave module in the write binary mode
    obj = wave.open("new_record.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setframerate(RATE)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.writeframes(b"".join(frames))
    obj.close()

# constants
RATE = 16_000
FRAMES_PER_BUFFER =3_200
CHANNELS = 1
FORMAT = pyaudio.paInt16


audio_recording(RATE, FRAMES_PER_BUFFER, CHANNELS, FORMAT)