import io
import speech_recognition as sr
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", language_code: str = "te-IN") -> str:
        """Transcribes physical audio streams using local zero-cost processing libraries supporting global language matrices."""
        audio_io = io.BytesIO(audio_bytes)
        
        # Native WAV PCM checking pass
        if audio_format.lower() == "wav":
            try:
                with sr.AudioFile(audio_io) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_data = self.recognizer.record(source)
                # Map target code explicitly
                target_lang = "" if language_code == "auto" else language_code
                return self.recognizer.recognize_google(audio_data, language=target_lang)
            except Exception:
                audio_io.seek(0)

        # Compressed stream asset parsing track
        try:
            from pydub import AudioSegment
            audio_segment = AudioSegment.from_file(audio_io, format=audio_format.lower())
            
            raw_wav_io = io.BytesIO()
            audio_segment.export(raw_wav_io, format="wav")
            raw_wav_io.seek(0)
            
            with sr.AudioFile(raw_wav_io) as source:
                self.recognizer.dynamic_energy_threshold = False
                self.recognizer.energy_threshold = 100
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = self.recognizer.record(source)
                
            # If "auto" is chosen, let the endpoint guess, otherwise enforce explicit regional codes
            target_lang = "" if language_code == "auto" else language_code
            return self.recognizer.recognize_google(audio_data, language=target_lang)
            
        except FileNotFoundError as e:
            if "ffprobe" in str(e) or "ffmpeg" in str(e):
                return "☁️ Web Cloud Setup Required: Please add a 'packages.txt' file containing the word 'ffmpeg' to your main repository so the platform can process compressed audio formats."
            return f"Audio Read Exception: {str(e)}"
        except Exception as general_err:
            return f"Transcription Warning: Sound captured, but audio content could not be converted smoothly: {str(general_err)}"
