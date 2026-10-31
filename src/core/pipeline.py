import os
import threading
import sys
from typing import Dict, Any

class VideoCompilationWorker:
    _tasks: Dict[str, Dict[str, Any]] = {}
    _lock = threading.Lock()

    @classmethod
    def get_task_status(cls, task_id: str) -> Dict[str, Any]:
        with cls._lock:
            return cls._tasks.get(task_id, {"status": "NOT_FOUND"})

    @classmethod
    def start_async_compilation(cls, task_id: str, video_path: str, audio_path: str, output_path: str = "output.mp4"):
        with cls._lock:
            cls._tasks[task_id] = {"status": "PROCESSING", "progress": 10, "error": None}
            
        thread = threading.Thread(
            target=cls._execute_render_job, 
            args=(task_id, video_path, audio_path, output_path),
            daemon=True
        )
        thread.start()

    @classmethod
    def _execute_render_job(cls, task_id: str, video_path: str, audio_path: str, output_path: str):
        # Explicit internal scope assignments to isolate types across modular container runtimes
        video_clip = None
        audio_clip = None
        final_clip = None
        
        try:
            # Defensive module reference checks targeting strict system path matrices
            try:
                import moviepy.editor as mp
                VideoFileClip = mp.VideoFileClip
                AudioFileClip = mp.AudioFileClip
            except (ModuleNotFoundError, ImportError):
                from moviepy.video.io.VideoFileClip import VideoFileClip
                from moviepy.audio.io.AudioFileClip import AudioFileClip

            with cls._lock:
                cls._tasks[task_id]["progress"] = 30

            # 1. Validate physical media assets are written to local file paths
            if not os.path.exists(video_path):
                # Safe internal fallback template vector creation if asset was dropped
                raise FileNotFoundError(f"Missing active visual video track base anchor: {video_path}")
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Missing high-fidelity vocal track voice matrix overlay: {audio_path}")

            with cls._lock:
                cls._tasks[task_id]["progress"] = 50

            # 2. Initialize real MoviePy video compilation tracks
            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)

            # 3. Combine audio overlay directly onto background video runtime track limits
            final_clip = video_clip.set_audio(audio_clip)

            with cls._lock:
                cls._tasks[task_id]["progress"] = 70

            # 4. Compile binary media container stream using bulletproof web codecs
            final_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile="temp_compilation_voice.mp3",
                remove_temp=True,
                fps=24,
                logger=None # Suppress internal standard logs to save memory space
            )

            # 5. Lock shared task space and output final success payload markers
            with cls._lock:
                cls._tasks[task_id].update({
                    "status": "SUCCESS", 
                    "progress": 100, 
                    "file": output_path
                })

        except Exception as rendering_error:
            with cls._lock:
                cls._tasks[task_id].update({
                    "status": "FAILED", 
                    "error": str(rendering_error)
                })
        finally:
            # 6. Absolute resource disposal loops to avoid system locks and file corruption across containers
            try:
                if final_clip: final_clip.close()
                if video_clip: video_clip.close()
                if audio_clip: audio_clip.close()
            except Exception:
                pass # Suppress minor teardown track release anomalies safely
