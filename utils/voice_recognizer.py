class Voice():

    def __init__(self):
        self.threshold = 1350
        self.chunk = 1024
        self.fs = 44100
        self.p = pyaudio.PyAudio
        self.sample_format = pyaudio.paInt16

    def create_recognizer(self):
        return sr.Recognizer()

    def get_mic(self):
        return sr.Microphone(device_index = 0)

    def get_text(self):
        r = create_recognizer()
        with self.get_mic() as source:
            audio = r.listen(source, timeout = 3)
        return r.recognize_google(audio)

    def get_stream(self):
        return self.p.open(format = self.sample_format,
                    channels = 1,
                    rate = 44100,
                    input = True,
                    frames_per_buffer = self.chunk)

    def initialize_recognition(self):
        chunk_count = 0
        user_input = []
        while True:
            stream = self.get_stream()
            data = stream.read(self.chunk, exception_on_overflow = False)
            if audio.rms(data, 2) > self.threshold:
                chunk_count += 1
            else:
                chunk_count = 0
            if chunk_count >= 5:
                try:
                    print('Chrome is listening!')
                    text = self.get_text().lower()
                    if 'chrome' in text:
                        user_input.append(text)
                    if 'cancel' in text:
                        break
                    else:
                        pass
                except:
                    pass
        return user_input
