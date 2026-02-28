import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 10,
                host=os.getenv("DB_HOST", "localhost"),
                database=os.getenv("DB_NAME", "knowledgequest"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASS", "postgres")
            )
            cls._instance.init_db()
        return cls._instance

    def get_connection(self):
        return self.connection_pool.getconn()

    def release_connection(self, conn):
        self.connection_pool.putconn(conn)

    def init_db(self):
        """Initializes pgvector and create the embeddings table if it doesn't exist."""
        sql = """
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE TABLE IF NOT EXISTS embeddings (
            id SERIAL PRIMARY KEY,
            id_document TEXT,
            texte_fragment TEXT,
            vecteur VECTOR(384)
        );
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
        finally:
            self.release_connection(conn)

    def insert_batch(self, data_list):
        """
        data_list: list of tuples (id_document, texte_fragment, vecteur)
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.executemany(
                    "INSERT INTO embeddings (id_document, texte_fragment, vecteur) VALUES (%s, %s, %s)",
                    data_list
                )
            conn.commit()
        finally:
            self.release_connection(conn)

    def search(self, query_embedding, top_k=3):
        """
        Performs vector search using cosine similarity.
        Cosine similarity = 1 - (vecteur <=> query_embedding)
        """
        sql = """
        SELECT id_document, texte_fragment, 1 - (vecteur <=> %s::vector) AS similarity
        FROM embeddings
        ORDER BY similarity DESC
        LIMIT %s;
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (query_embedding.tolist(), top_k))
                return cur.fetchall()
        finally:
            self.release_connection(conn)
