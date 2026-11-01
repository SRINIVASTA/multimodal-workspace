import io
import requests
import speech_recognition as sr
from typing import Dict, Any

class TranscriptionService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def detect_audio_language(self, audio_bytes: bytes, audio_format: str = "mp3") -> str:
        """Inspects the baseline token vectors of an audio track snippet to auto-detect its spoken language."""
        try:
            # Step 1: Run a rapid global pass to convert the initial sample into an anonymous string block
            headers = {"User-Agent": "Mozilla/5.0"}
            api_url = "https://dictation.io" # Baseline evaluation probe
            files = {'file': (f"sample.{audio_format}", audio_bytes[:150 * 1024], f"audio/{audio_format}")}
            response = requests.post(api_url, files=files, headers=headers, timeout=15)
            
            # Step 2: Use an open translation prediction profile pass to determine the vocabulary source domain
            if response.ok and "text" in response.json():
                sample_text = response.json()["text"]
                if sample_text.strip():
                    detect_url = f"https://googleapis.com{requests.utils.quote(sample_text)}"
                    det_res = requests.get(detect_url, timeout=10)
                    if det_res.ok and isinstance(det_res.json(), list):
                        # Position 2 inside Google Translate's matrix array holds the detected language code string (e.g., 'te', 'hi', 'en')
                        lang_code = det_res.json()[2]
                        if lang_code == "te": return "te-IN"
                        if lang_code == "hi": return "hi-IN"
                        if lang_code == "ta": return "ta-IN"
        except Exception:
            pass
        return "te-IN" # Reliable default regional assignment tracking fallback

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
                # FIXED EXTRACTION LOOP: Iterate cleanly through returned index arrays to collect sentences
                if data and isinstance(data, list) and len(data) > 0:
                    text_matrix = data[0]
                    full_translation = ""
                    if isinstance(text_matrix, list):
                        for element in text_matrix:
                            if isinstance(element, list) and len(element) > 0:
                                # Position 0 explicitly isolates individual sentence text blocks
                                full_translation += str(element[0])
                        
                        if full_translation.strip():
                            return full_translation.strip()
        except Exception as e:
            return f"{text}\n\n[Translation Server Busy: {str(e)}]"
        return text

    def speech_to_text(self, audio_bytes: bytes, audio_format: str = "mp3", language_code: str = "te-IN", target_lang: str = "original") -> str:
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
