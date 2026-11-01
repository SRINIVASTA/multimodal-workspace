import io
import requests
import speech_recognition as sr
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def _extract_translated_string(self, obj) -> str:
        """Recursively drills down into any nested list array structure to find strings."""
        if isinstance(obj, list) and len(obj) > 0:
            # In Google's structure, the first element of the first list holds the text block
            first_element = obj[0]
            if isinstance(first_element, list):
                return self._extract_translated_string(first_element)
            elif isinstance(first_element, str):
                return first_element
        return ""

    def _translate_text(self, text: str, target_lang: str) -> str:
        """Helper method to isolate and parse the exact translation text matrix segments cleanly."""
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
                # Use recursive extraction to capture the deep structural string layer
                translated_result = self._extract_translated_string(data)
                if translated_result and translated_result.strip():
                    return translated_result.strip()
        except Exception as e:
            return f"{text}\n\n[Translation Server Busy: {str(e)}]"
        return text

    def detect_audio_language(self, audio_bytes: bytes, audio_format: str = "mp3") -> str:
        """Accurately identifies the spoken language domain by analyzing an initial audio snippet."""
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            api_url = "https://dictation.io"
            files = {'file': (f"detect.{audio_format}", audio_bytes[:200 * 1024], f"audio/{audio_format}")}
            response = requests.post(api_url, files=files, headers=headers, timeout=12)
            
            if response.ok and "text" in response.json():
                sample_text = response.json()["text"].strip()
                if sample_text:
                    detect_url = f"https://googleapis.com"
                    params = {"client": "gtx", "sl": "auto", "tl": "en", "dt": "t", "q": sample_text}
                    det_res = requests.get(detect_url, params=params, timeout=10)
                    
                    if det_res.ok and isinstance(det_res.json(), list):
                        raw_payload = det_res.json()
                        if len(raw_payload) > 2 and isinstance(raw_payload[2], str):
                            detected_slug = raw_payload[2].lower()
                            if "te" in detected_slug: return "te-IN"
                            if "hi" in detected_slug: return "hi-IN"
                            if "ta" in detected_slug: return "ta-IN"
                            if "en" in detected_slug: return "en-US"
                            return f"{detected_slug}-IN" if len(detected_slug) == 2 else "en-US"
        except Exception:
            pass
        return "en-US"

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", language_code: str = "en-US", target_lang: str = "original") -> str:
        """Transcribes any dynamic format and handles automatic translation transformations seamlessly."""
        audio_io = io.BytesIO(audio_bytes)
        speech_lang = language_code

        raw_text = ""
        if audio_format.lower() == "wav":
            try:
                with sr.AudioFile(audio_io) as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio_data = self.recognizer.record(source)
                raw_text = self.recognizer.recognize_google(audio_data, language=speech_lang)
            except Exception:
                audio_io.seek(0)

        if not raw_text:
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
                    
                raw_text = self.recognizer.recognize_google(audio_data, language=speech_lang)
                
            except (FileNotFoundError, ImportError):
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    api_url = f"https://dictation.io{speech_lang}"
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

        return self._translate_text(raw_text, target_lang)
