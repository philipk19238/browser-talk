import pyaudio
import audioop
import speech_recognition as sr


def create_recognizer():
    return sr.Recognizer()

def get_mic():
    return sr.Microphone(device_index = 0)

def get_text(mic):
    r = create_recognizer()
    with mic as source:
        audio = r.listen(source, timeout = 1.25)
    return r.recognize_google(audio)

    
THRESHOLD = 1350
CHUNK = 1024
fs = 44100
seconds = 3
filename = 'output.wav'
channels = 2
sample_format = pyaudio.paInt16

p = pyaudio.PyAudio()
stream = p.open(format=sample_format,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer = CHUNK)


counter = 0
mic = get_mic()
while True:
    data = stream.read(CHUNK, exception_on_overflow=False)
    if audioop.rms(data, 2) > THRESHOLD:
        counter += 1
    else:
        counter = 0
    if counter >= 5:
        print("Working.")
        try:
            text = get_text(mic)
            print(text)
        except sr.UnknownValueError or sr.WaitTimeoutError:
            pass
        counter = 0
       
