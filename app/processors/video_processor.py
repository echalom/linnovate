import whisper
from moviepy.editor import VideoFileClip

class VideoProcessor:
    def __init__(self):
        self.audio_model = whisper.load_model("base")

    def extract_audio_text(self, video_path):
        result = self.audio_model.transcribe(video_path)
        return result['text']

    def extract_key_moments(self, video_path):
        # For demonstration, we simulate:
        return [
            (5.0, "Explosion detected"),
            (15.0, "People speaking detected"),
            (25.0, "Vehicle movement detected")
        ]
