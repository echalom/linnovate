import os
from database.db_manager import DBManager
from llm.llm_client import LLMClient
from processors.video_processor import VideoProcessor

def main():
    print(" here 1\n", flush=True)
    db = DBManager(user="postgres", password="postgres", db="videos", host="postgres")
    print(" here 2\n", flush=True)
    llm = LLMClient()
    print(" here 3\n", flush=True)
    processor = VideoProcessor()
    print(" here 4\n", flush=True)

    # video_path = "sample.mp4"
    # video_path = "sample2.mp4"
    video_path = "../sample2.mp4"
    video_id = "demo_video_001"

    print("🟩 Extracting audio...")
    audio_text = processor.extract_audio_text(video_path)

    print("🟩 Extracting key moments...")
    key_moments = processor.extract_key_moments(video_path)

    for timestamp, event_desc in key_moments:
        combined_text = f"{event_desc}. Audio snippet: {audio_text[:200]}"
        embedding = llm.generate_embedding(combined_text)
        summary = llm.generate_summary(combined_text)

        db.insert_highlight(video_id, timestamp, combined_text, embedding, summary)
        print(f"✅ Inserted highlight at {timestamp}s: {event_desc}")

    print("✅ All highlights inserted.\n")
    print("🟩 Running example similarity search:")
    query_embedding = llm.generate_embedding("explosion and vehicle")
    results = db.similarity_search(query_embedding, top_k=3)
    for r in results:
        print(f"Found: VideoID={r[0]}, Timestamp={r[1]}, Desc={r[2][:60]}, Summary={r[3][:60]}")

if __name__ == "__main__":
    main()
