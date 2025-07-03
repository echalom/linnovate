import os
from database.db_manager import DBManager
from llm.llm_client import LLMClient
from processors.video_processor import VideoProcessor

def main():
    print("🟩 Connecting to database...")
    db = DBManager(user="postgres", password="postgres", db="videos", host="postgres")
    print("✅ Database connected.\n")

    print("🟩 Loading LLM client...")
    llm = LLMClient()
    print("✅ LLM client ready.\n")

    print("🟩 Loading Video Processor...")
    processor = VideoProcessor()
    print("✅ Video Processor ready.\n")

    # Set the video file you want to process
    video_file_list = ['sample.mp4', 'sample_8.mp4', 'sample_7.mp4', 'sample_6.mp4',
     'sample5.mp4', 'sample2.mp4']
    for video_path in video_file_list:
        video_id = video_path

        print("processing ", video_id+':\n')
        print("🟩 Extracting audio transcript...\n")
        audio_text = processor.extract_audio_text(video_path)
        print(f"✅ Audio transcript extracted (first 200 chars): {audio_text[:200]}...\n", flush=True)

        print("🟩 Extracting scene-level descriptions...\n")
        key_moments = processor.extract_key_moments(video_path)

        print("🟩 Inserting highlights into PGVector...\n")
        for timestamp, event_desc in key_moments:
            combined_text = f"Scene description: {event_desc}. Audio snippet: {audio_text[:200]}"
            embedding = llm.generate_embedding(combined_text)
            summary = llm.generate_summary(combined_text)

            db.insert_highlight(video_id, timestamp, combined_text, embedding, summary)
            print(f"✅ Inserted highlight at {timestamp:.2f}s: {event_desc[:80]}...")

        print("\n✅ All highlights inserted into database.\n")

        print("🟩 Running example semantic similarity search for 'explosion and vehicle'...\n")
        query_embedding = llm.generate_embedding("explosion and vehicle")
        results = db.similarity_search(query_embedding, top_k=3)

        if results:
            for r in results:
                print(f"Found: VideoID={r[0]}, Timestamp={r[1]:.2f}s, Desc={r[2][:60]}..., Summary={r[3][:60]}...")
        else:
            print("No similar highlights found.\n")

        print("\n✅ Pipeline completed.\n")

if __name__ == "__main__":
    main()
