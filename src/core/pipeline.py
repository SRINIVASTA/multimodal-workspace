import os
from moviepy.editor import VideoFileClip, AudioFileClip

class VideoCompilationWorker:
    @staticmethod
    def compile_commercial(video_path: str, audio_path: str, output_path: str = "output.mp4") -> str:
        if not os.path.exists(video_path) or not os.path.exists(audio_path):
            raise FileNotFoundError("Required media streams could not be identified locally.")
        
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        
        # Scale video clip length to match synthesized voice track track length
        if video_clip.duration < audio_clip.duration:
            video_clip = video_clip.loop(duration=audio_clip.duration)
        else:
            video_clip = video_clip.subclip(0, audio_clip.duration)
            
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
        return output_path
