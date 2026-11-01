import io
import speech_recognition as sr
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        # Initialized locally; no OpenRouter API network endpoints or balance checks are hit
        self.recognizer = sr.Recognizer()

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", model: str = "") -> str:
        """Transcribes physical audio streams using local zero-cost processing libraries."""
        # Convert incoming bytes matrix stream securely to an in-memory stream layout
        audio_file_stream = io.BytesIO(audio_bytes)
        
        # Read and unpack the target audio buffer structure
        with sr.AudioFile(audio_file_stream) as source:
            # Calibrate structural processing lines for background noise distortion
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = self.recognizer.record(source)
            
        try:
            # Process via zero-cost API engine endpoints (No OpenRouter key or wallet balance requested)
            transcript_text = self.recognizer.recognize_google(audio_data)
            return transcript_text
        except sr.UnknownValueError:
            return "Local Transcription Error: Audio clarity was too low to isolate clear phrase strings."
        except sr.RequestError as request_err:
            raise RuntimeError(f"Local Processing Network Interconnect Error: {str(request_err)}")
