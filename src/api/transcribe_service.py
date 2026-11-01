import io
import requests
import speech_recognition as sr
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def _translate_text(self, text: str, target_lang: str) -> str:
        """Helper method to isolate and parse the exact translation from the API array matrix."""
        if not text or target_lang == "original" or text.startswith("☁️") or "Transcription Warning" in text:
            return text
        try:
            base_url = "https://googleapis.com"
            query_params = {
                "client": "gtx",
                "sl": "auto",
                "tl": target_lang,
                "dt": "t",
                "q": text
            }
            
            res = requests.get(base_url, params=query_params, timeout=10)
            if res.ok:
                data = res.json()
                # ROBUST FIX: Drill directly into the nested translation array structures safely
                if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                    full_translation = ""
                    for sentence_block in data[0]:
                        if isinstance(sentence_block, list) and len(sentence_block) > 0:
                            # Position 0 inside each sub-array contains the actual translated piece
                            full_translation += str(sentence_block[0])
                    
                    if full_translation.strip():
                        return full_translation.strip()
        except Exception as e:
            return f"{text}\n\n[Translation Server Busy: {str(e)}]"
        return text

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", language_code: str = "auto", target_lang: str = "original") -> str:
        """Transcribes any dynamic format and handles automatic translation transformations seamlessly."""
        audio_io = io.BytesIO(audio_bytes)
        speech_lang = "" if language_code == "auto" else language_code

        # Track 1: Uncompressed WAV fallback logic pass
        raw_text = ""
        if audio_format.lower() == "wav":
            try:
                with sr.AudioFile(audio_io) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_data = self.recognizer.record(source)
                raw_text = self.recognizer.recognize_google(audio_data, language=speech_lang)
            except Exception:
                audio_io.seek(0)

        # Track 2: Local pydub transcoder block if ffmpeg dependencies exist
        if not raw_text:
            try:
                from pydub import AudioSegment
                audio_segment = AudioSegment.from_file(audio_io, format=audio_format.lower())
                
                raw_wav_io = io.BytesIO()
                audio_segment.export(raw_wav_io, format="wav")
                raw_wav_io.seek(0)
                
                with sr.AudioFile(raw_wav_io) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_data = self.recognizer.record(source)
                    
                raw_text = self.recognizer.recognize_google(audio_data, language=speech_lang)
                
            except (FileNotFoundError, ImportError):
                # Track 3: Online cloud proxy fallback for serverless hosting frames
                try:
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                    api_url = f"https://dictation.io{speech_lang if speech_lang else 'en-US'}"
                    files = {'file': (f"audio.{audio_format}", audio_bytes, f"audio/{audio_format}")}
                    response = requests.post(api_url, files=files, headers=headers, timeout=30)
                    if response.ok and "text" in response.json():
                        raw_text = response.json()["text"]
                except Exception:
                    pass
                
                if not raw_text:
                    return (
                        "☁️ Cloud Environment Setup Needed: To transcribe compressed formats directly in the cloud, "
                        "please create a new file named 'packages.txt' in your main GitHub repository root folder, "
                        "write the single word 'ffmpeg' inside it, and save it."
                    )
            except Exception as general_err:
                return f"Transcription Warning: Sound captured, but audio content could not be parsed: {str(general_err)}"

        # Run translation transformation logic mapping pass before passing strings back to the interface layout
        return self._translate_text(raw_text, target_lang)
