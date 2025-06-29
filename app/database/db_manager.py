import psycopg2
from pgvector.psycopg2 import register_vector
import numpy as np

class DBManager:
    def __init__(self, user, password, db, host='postgres', port='5432'):
        self.conn = psycopg2.connect(
            dbname=db,
            user=user,
            password=password,
            host=host,
            port=port
        )
        register_vector(self.conn)
        self.create_table()

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS highlights (
                    id SERIAL PRIMARY KEY,
                    video_id TEXT,
                    timestamp FLOAT,
                    description TEXT,
                    embedding VECTOR(384),
                    summary TEXT
                );
            """)
            self.conn.commit()

    def insert_highlight(self, video_id, timestamp, description, embedding, summary):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO highlights (video_id, timestamp, description, embedding, summary) VALUES (%s, %s, %s, %s, %s)",
                (video_id, timestamp, description, embedding.tolist(), summary)
            )
            self.conn.commit()

    def similarity_search(self, query_embedding, top_k=3):
        with self.conn.cursor() as cur:
            cur.execute(
                "SELECT video_id, timestamp, description, summary FROM highlights ORDER BY embedding <-> %s::vector LIMIT %s",
                (query_embedding.tolist(), top_k)
            )
            return cur.fetchall()
