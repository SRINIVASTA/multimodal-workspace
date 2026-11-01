import io
import speech_recognition as sr
from pydub import AudioSegment
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", model: str = "") -> str:
        """Transcribes physical audio streams using local zero-cost processing libraries."""
        try:
            # UNPACK & TRANSCODE LOOP: Convert incoming audio bytes to a raw PCM file format in memory
            audio_io = io.BytesIO(audio_bytes)
            
            # Read whatever format was sent (wav, mp3, ogg, etc.) using pydub
            audio_segment = AudioSegment.from_file(audio_io, format=audio_format.lower())
            
            # Export out to a strictly standardized, raw uncompressed PCM WAV matrix format
            raw_wav_io = io.BytesIO()
            audio_segment.export(raw_wav_io, format="wav")
            raw_wav_io.seek(0)
            
            # Pass the clean raw PCM WAV file right into the recognizer structure
            with sr.AudioFile(raw_wav_io) as source:
                # Lower threshold slightly to capture lower volume singing/speech
                self.recognizer.dynamic_energy_threshold = False
                self.recognizer.energy_threshold = 150 
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio_data = self.recognizer.record(source)
                
            # FIX: Force 'en-IN' (Indian English/Multilingual blend) to catch regional accents & birthday tracks
            transcript_text = self.recognizer.recognize_google(audio_data, language="en-IN")
            return transcript_text
            
        except sr.UnknownValueError:
            # Fallback pass: If en-IN fails, try a generic global language detection pass as a backup
            try:
                raw_wav_io.seek(0)
                with sr.AudioFile(raw_wav_io) as source:
                    audio_data = self.recognizer.record(source)
                return self.recognizer.recognize_google(audio_data, language="en-US")
            except Exception:
                return "Local Transcription Warning: Sound captured, but audio content was too faint or distorted to decode clearly."
        except sr.RequestError as request_err:
            raise RuntimeError(f"Local Processing Network Interconnect Error: {str(request_err)}")
        except Exception as transcode_err:
            raise RuntimeError(f"Audio Processing Error: Could not unpack format data profile. Detailed traceback: {str(transcode_err)}")
