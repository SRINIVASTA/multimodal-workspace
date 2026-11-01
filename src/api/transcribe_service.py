import io
import requests
import speech_recognition as sr
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def detect_audio_language(self, audio_bytes: bytes, audio_format: str = "mp3") -> str:
        """Accurately identifies the spoken language domain by analyzing an initial audio snippet."""
        try:
            # Step 1: Run an immediate fast pass to read a tiny slice with standard en-US parameters
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            api_url = "https://dictation.io"
            # Read a 200KB chunk for language classification metrics
            files = {'file': (f"detect.{audio_format}", audio_bytes[:200 * 1024], f"audio/{audio_format}")}
            response = requests.post(api_url, files=files, headers=headers, timeout=12)
            
            if response.ok and "text" in response.json():
                sample_text = response.json()["text"].strip()
                if sample_text:
                    # Step 2: Query the linguistic signature engine to pull the absolute source language code
                    detect_url = f"https://googleapis.com"
                    params = {"client": "gtx", "sl": "auto", "tl": "en", "dt": "t", "q": sample_text}
                    det_res = requests.get(detect_url, params=params, timeout=10)
                    
                    if det_res.ok and isinstance(det_res.json(), list):
                        raw_payload = det_res.json()
                        # Position index 2 inside Google Translate's API reliably exposes the true source language string
                        if len(raw_payload) > 2 and isinstance(raw_payload[2], str):
                            detected_slug = raw_payload[2].lower()
                            if "te" in detected_slug: return "te-IN"
                            if "hi" in detected_slug: return "hi-IN"
                            if "ta" in detected_slug: return "ta-IN"
                            if "en" in detected_slug: return "en-US"
                            # Dynamic auto-routing for other detected foreign profiles
                            return f"{detected_slug}-IN" if len(detected_slug) == 2 else "en-US"
        except Exception:
            pass
        
        # If the scan times out, we return en-US as a safe base standard instead of blindly sticking to Telugu
        return "en-US"

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
                if data and isinstance(data, list) and len(data) > 0:
                    # Parse through sentences to build the final translation string
                    first_block = data[0]
                    full_translation = ""
                    if isinstance(first_block, list):
                        for sentence_block in first_block:
                            if isinstance(sentence_block, list) and len(sentence_block) > 0:
                                # Position 0 contains the translated text fragment
                                full_translation += str(sentence_block[0])
                        
                        if full_translation.strip():
                            return full_translation.strip()
        except Exception as e:
            return f"{text}\n\n[Translation Server Busy: {str(e)}]"
        return text

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
