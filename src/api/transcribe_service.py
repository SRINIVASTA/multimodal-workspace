import io
import requests
import speech_recognition as sr
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def _translate_text(self, text: str, target_lang: str) -> str:
        """Helper method to isolate and parse translations instantly using flat JSON properties with auto-detection."""
        if not text or target_lang == "original" or text.startswith("☁️") or "With Size Optimization" in text:
            return text
        try:
            # Shift translation pipeline to use a flat JSON endpoint architecture
            base_url = "https://translated.net"
            query_params = {
                "q": text,
                # FIX: Force source language to 'auto' so it dynamically captures any input string format (US English, Indian English, etc.)
                "langpair": f"auto|{target_lang}"  
            }
            
            res = requests.get(base_url, params=query_params, timeout=10)
            if res.ok:
                response_json = res.json()
                # Direct lookup on flat key string property value matrices
                if "responseData" in response_json and "translatedText" in response_json["responseData"]:
                    translated_string = response_json["responseData"]["translatedText"]
                    if translated_string and translated_string.strip() != text.strip():
                        return translated_string.strip()
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
                    base_url = "https://translated.net"
                    query_params = {"q": sample_text, "langpair": "auto|en"}
                    det_res = requests.get(base_url, params=query_params, timeout=10)
                    if det_res.ok:
                        res_data = det_res.json()
                        if "matches" in res_data and len(res_data["matches"]) > 0:
                            detected_slug = res_data["matches"][0].get("language", "en").lower()
                            if "te" in detected_slug: return "te-IN"
                            if "hi" in detected_slug: return "hi-IN"
                            if "ta" in detected_slug: return "ta-IN"
                            if "en" in detected_slug: return "en-US"
        except Exception:
            pass
        return "en-US"

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", language_code: str = "en-US", target_lang: str = "original") -> str:
        """Transcribes any dynamic format natively using zero-cost web frameworks."""
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
