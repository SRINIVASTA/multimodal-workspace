import os
import time
import threading
from typing import Dict, Any

class VideoCompilationWorker:
    # Global thread safe tracker to follow background processing task parameters
    _tasks: Dict[str, Dict[str, Any]] = {}
    _lock = threading.Lock()

    @classmethod
    def get_task_status(cls, task_id: str) -> Dict[str, Any]:
        """Thread-safe lookups into active rendering jobs."""
        with cls._lock:
            return cls._tasks.get(task_id, {"status": "NOT_FOUND"})

    @classmethod
    def start_async_compilation(cls, task_id: str, video_path: str, audio_path: str, output_path: str = "output.mp4"):
        """Dispatches an isolated background worker thread to execute heavy moviepy tasks."""
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
        """Internal worker method executed away from Streamlit's rendering event loop loops."""
        try:
            # Lazy load massive binary video processing packages only during active execution windows
            from moviepy.editor import VideoFileClip, AudioFileClip
            
            if not os.path.exists(video_path) or not os.path.exists(audio_path):
                raise FileNotFoundError("Target asset media streams not located on storage disks.")

            with cls._lock:
                cls._tasks[task_id]["progress"] = 40

            video_clip = VideoFileClip(video_path)
            audio_clip = AudioFileClip(audio_path)
            
            if video_clip.duration < audio_clip.duration:
                video_clip = video_clip.loop(duration=audio_clip.duration)
            else:
                video_clip = video_clip.subclip(0, audio_clip.duration)
                
            final_clip = video_clip.set_audio(audio_clip)
            
            with cls._lock:
                cls._tasks[task_id]["progress"] = 70
                
            final_clip.write_videofile(
                output_path, 
                fps=24, 
                codec="libx264", 
                audio_codec="aac", 
                logger=None  # Suppresses dense internal trace messaging outputs
            )

            # Properly release system file descriptors
            video_clip.close()
            audio_clip.close()
            final_clip.close()

            with cls._lock:
                cls._tasks[task_id].update({"status": "SUCCESS", "progress": 100, "file": output_path})

        except Exception as e:
            with cls._lock:
                cls._tasks[task_id].update({"status": "FAILED", "error": str(e)})
