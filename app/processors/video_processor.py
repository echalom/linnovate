import whisper
from moviepy import VideoFileClip
import cv2
import numpy as np
from scenedetect import SceneManager, open_video, ContentDetector
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

class VideoProcessor:
    def __init__(self):
        print('processor here 1', flush=True)
        self.audio_model = whisper.load_model("base")
        print('processor here 2', flush=True)

        print("Loading BLIP for image captioning...", flush=True)
        self.caption_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        self.caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        print("BLIP loaded.", flush=True)

    def extract_audio_text(self, video_path):
        result = self.audio_model.transcribe(video_path)
        return result['text']

    def extract_key_moments(self, video_path):
        """
        Scene-level extraction using scenedetect + BLIP captioning.
        Returns: List of (timestamp, scene_description)
        """
        video = open_video(video_path)
        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold=30.0))
        scene_manager.detect_scenes(video)
        scene_list = scene_manager.get_scene_list()

        key_moments = []

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)

        for i, (start_time, end_time) in enumerate(scene_list):
            start_frame = int(start_time.get_seconds() * fps)
            end_frame = int(end_time.get_seconds() * fps)
            num_frames = max(1, end_frame - start_frame)

            frame_indices = np.linspace(start_frame, end_frame - 1, num=min(5, num_frames), dtype=int)
            captions = []

            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if not ret:
                    continue
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img)

                inputs = self.caption_processor(images=pil_img, return_tensors="pt")
                out = self.caption_model.generate(**inputs)
                caption = self.caption_processor.decode(out[0], skip_special_tokens=True)
                captions.append(caption)

            scene_description = " ".join(captions)
            timestamp = start_time.get_seconds()
            key_moments.append((timestamp, scene_description))
            print(f"Scene {i+1} ({start_time} - {end_time}): {scene_description}", flush=True)

        cap.release()
        return key_moments
