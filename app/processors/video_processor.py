import os
import wave
import json
from moviepy import VideoFileClip
from scenedetect import SceneManager, open_video, ContentDetector
from scenedetect.scene_manager import save_images
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

    # def extract_key_moments(self, video_path):
    #     # Placeholder: Enhance with scene detection if desired
    #     return [
    #         (5.0, "Key moment detected"),
    #         (15.0, "Another interesting event")
    #     ]

    def extract_key_moments(self, video_path):
        """
        Uses PySceneDetect to detect scenes and generates simple scene descriptions.
        Returns a list of (timestamp, description) tuples for each scene boundary.
        """
        print("🟩 Running scene detection...\n", flush=True)
        video = open_video(video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=30.0))
        scene_manager.detect_scenes(video)
        scene_list = scene_manager.get_scene_list()

        key_moments = []
        for i, (start_time, end_time) in enumerate(scene_list):
            mid_time = start_time.get_seconds() + (end_time.get_seconds() - start_time.get_seconds()) / 2
            description = f"Scene {i+1} from {start_time} to {end_time} likely contains activity."
            key_moments.append((mid_time, description))

        if not key_moments:
            # fallback if no scenes detected
            key_moments = [(5.0, "Default: Entire clip considered as a single scene.")]

        print(f"✅ Detected {len(key_moments)} scenes.\n", flush=True)
        return key_moments