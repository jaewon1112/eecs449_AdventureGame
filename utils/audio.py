import whisper
import pyttsx3
import sounddevice as sd
import wave

class AudioHandler:
    def __init__(self):
        self.model = whisper.load_model("base")  # Whisper 모델 로드
        self.engine = pyttsx3.init()  # TTS 엔진 초기화
    
    def record_audio(self, filename="input.wav", duration=5):
        # 음성 녹음
        fs = 16000  # 샘플링 레이트
        print("Recording...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(recording.tobytes())
        return filename
    
    def transcribe(self, audio_path):
        # 음성 → 텍스트 변환
        result = self.model.transcribe(audio_path)
        return result["text"]
    
    def speak(self, text):
        # 텍스트 → 음성 출력
        self.engine.say(text)
        self.engine.runAndWait()
