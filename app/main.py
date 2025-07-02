import os
from database.db_manager import DBManager
from llm.llm_client import LLMClient
from processors.video_processor import VideoProcessor

def main():
    print("🟩 Connecting to database...", flush=True)
    db = DBManager(user="postgres", password="postgres", db="videos", host="postgres")
    print("✅ Database connected.\n", flush=True)

    print("🟩 Loading LLM client...", flush=True)
    llm = LLMClient()
    print("✅ LLM client ready.\n", flush=True)

    print("🟩 Loading Video Processor...", flush=True)
    processor = VideoProcessor()
    print("✅ Video Processor ready.\n", flush=True)

    # Set the video file you want to process
    video_path = "../sample_8.mp4"
    video_id = "demo_video_001"

    print("🟩 Extracting audio transcript...\n", flush=True)
    audio_text = processor.extract_audio_text(video_path)
    print(f"✅ Audio transcript extracted (first 200 chars): {audio_text[:200]}...\n", flush=True)

    print("🟩 Extracting scene-level descriptions...\n", flush=True)
    key_moments = processor.extract_key_moments(video_path)

    print("🟩 Inserting highlights into PGVector...\n", flush=True)
    for timestamp, event_desc in key_moments:
        combined_text = f"Scene description: {event_desc}. Audio snippet: {audio_text[:200]}"
        embedding = llm.generate_embedding(combined_text)
        summary = llm.generate_summary(combined_text)

        db.insert_highlight(video_id, timestamp, combined_text, embedding, summary)
        print(f"✅ Inserted highlight at {timestamp:.2f}s: {event_desc[:80]}...", flush=True)

    print("\n✅ All highlights inserted into database.\n", flush=True)

    print("🟩 Running example semantic similarity search for 'explosion and vehicle'...\n", flush=True)
    query_embedding = llm.generate_embedding("explosion and vehicle")
    results = db.similarity_search(query_embedding, top_k=3)

    if results:
        for r in results:
            print(f"Found: VideoID={r[0]}, Timestamp={r[1]:.2f}s, Desc={r[2][:60]}..., Summary={r[3][:60]}...", flush=True)
    else:
        print("No similar highlights found.\n", flush=True)

    print("\n✅ Pipeline completed.\n", flush=True)

if __name__ == "__main__":
    main()
