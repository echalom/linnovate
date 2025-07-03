import os
import wave
import json
from moviepy import VideoFileClip
from vosk import Model, KaldiRecognizer

class VideoProcessor:
    def __init__(self):
        print("🟩 Initializing Vosk model...")
        model_path = "vosk-model"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model not found at {model_path}")
        self.model = Model(model_path)
        print("✅ Vosk model loaded.")

    def extract_audio_text(self, video_path):
        print(f"🟩 Extracting audio from {video_path}...")
        clip = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        clip.audio.write_audiofile(audio_path, codec='pcm_s16le')

        wf = wave.open(audio_path, "rb")
        rec = KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)

        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                results.append(result.get('text', ''))
        final_result = json.loads(rec.FinalResult())
        results.append(final_result.get('text', ''))

        transcript = ' '.join(results)
        print("✅ Audio transcription complete.")
        return transcript

    def extract_key_moments(self, video_path):
        # Placeholder: Enhance with scene detection if desired
        return [
            (5.0, "Key moment detected"),
            (15.0, "Another interesting event")
        ]
