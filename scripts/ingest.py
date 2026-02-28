import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import glob
from pypdf import PdfReader
from docx import Document

from core.database import Database
from core.embedder import Embedder

def extract_text_from_pdf(path):
    try:
        reader = PdfReader(path)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        print(f"Error reading PDF {path}: {e}")
        return ""

def extract_text_from_docx(path):
    try:
        doc = Document(path)
        return " ".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading DOCX {path}: {e}")
        return ""

def extract_text_from_txt(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT {path}: {e}")
        return ""

def get_chunks(text, filename, chunk_size=80, overlap=15):
    words = text.split()
    chunks = []
    prefix = f"[Source: {filename}] "
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i:i + chunk_size]
        chunk_text = prefix + " ".join(chunk_words)
        chunks.append(chunk_text)
        if i + chunk_size >= len(words):
            break
    return chunks

def main():
    print("--- KnowledgeQuest Ingestion Started ---", flush=True)
    db = Database()
    embedder = Embedder()
    
    # Absolute path for Docker consistency
    data_dir = "/app/data"
    print(f"Target directory: {data_dir}", flush=True)

    if not os.path.exists(data_dir):
        print(f"ERROR: Directory '{data_dir}' not found!", flush=True)
        return

    all_data_to_insert = []
    files_found = 0

    print("Scanning for technical sheets...", flush=True)
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            files_found += 1
            file_path = os.path.join(root, file)
            filename = file
            ext = filename.split('.')[-1].lower() if '.' in filename else ''
            
            if ext in ['pdf', 'docx', 'txt']:
                print(f"Found match: {filename} (Ext: {ext})", flush=True)
                
                text = ""
                if ext == 'pdf':
                    text = extract_text_from_pdf(file_path)
                elif ext == 'docx':
                    text = extract_text_from_docx(file_path)
                elif ext == 'txt':
                    text = extract_text_from_txt(file_path)

                if text and text.strip():
                    chunks = get_chunks(text, filename)
                    embeddings = embedder.embed(chunks)
                    for text_chunk, vector in zip(chunks, embeddings):
                        all_data_to_insert.append((filename, text_chunk, vector.tolist()))
                    print(f"  -> Generated {len(chunks)} fragments.", flush=True)
                else:
                    print(f"  -> Warning: No text extracted from {filename}", flush=True)

    print(f"Scan complete. Total files seen: {files_found}", flush=True)
    
    if all_data_to_insert:
        print(f"Inserting {len(all_data_to_insert)} fragments into database...", flush=True)
        db.insert_batch(all_data_to_insert)
        print("✅ Ingestion successfully completed!", flush=True)
    else:
        print("❌ No valid text found to ingest. Check your data files.", flush=True)

if __name__ == "__main__":
    main()
