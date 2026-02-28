# 🏆 KnowledgeQuest RAG Module - Rose Blanche Group

KnowledgeQuest is a premium, gamified Retrieval-Augmented Generation (RAG) module designed to search technical sheets for bakery and pastry ingredients. It uses semantic search to provide highly relevant context and AI-generated deep exploration questions.

- Deployment Link: https://rag-ainightchallenge-eo8h92gtlguldfujzkafbm.streamlit.app/
- Demo Video: youtube.com/watch?v=iWKImK_a59M&feature=youtu.be
---

## 🚀 Quick Start (Recommended: Docker)

Using Docker is the fastest way to set up the system, including the PostgreSQL database with the `pgvector` extension.

### 1. Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.
- A **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/)).

### 2. Configuration
Create/Check the `.env` file in the root directory:
```env
DB_HOST=db
DB_NAME=knowledgequest
DB_USER=postgres
DB_PASS=postgres
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Launch Services
```bash
docker-compose up -d --build
```
This starts the database and the Streamlit app. Wait for them to be ready.

### 4. Ingest Technical Sheets
Place your PDFs, DOCXs, or TXTs in the `data/` folder (subfolders are supported). Then, run the ingestion script **inside the container**:
```bash
docker exec -it knowledgequest_app python scripts/ingest.py
```
*Wait for the "✅ Ingestion successfully completed!" message.*

### 5. Start Your Quest
Open your browser and visit:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🛠️ Tech Stack
- **Frontend**: Streamlit (Premium UI with custom CSS).
- **Database**: PostgreSQL + `pgvector` (Cosine Similarity search).
- **Embedding Model**: `all-MiniLM-L6-v2` (Sentence-Transformers).
- **LLM**: Groq API (Llama3-8b-8192) for follow-up questions.
- **Backend**: Python (Psycopg2, PyPDF, etc.).

---

## 🎮 Gamified Features
- **Match Strength Bars**: Real-time color-coded feedback on result relevance (Expert, Strong, or Weak matches).
- **Streak Counter**: Increases your streak for every high-quality query (>0.75 similarity).
- **Query Power Meter**: Rates your query length/descriptiveness (LOW, MID, MAX).
- **Deep Exploration**: AI-generated guided questions based on the top result for deeper learning.

---

## 🔍 Manual Setup (Alternative)

If you have PostgreSQL and `pgvector` installed locally:

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Setup DB**: Create a database named `knowledgequest` in your local Postgres.
3. **Run Ingestion**:
   ```bash
   python scripts/ingest.py
   ```
4. **Launch Streamlit**:
   ```bash
   streamlit run web/app.py
   ```

---

## 📂 Project Structure
- `core/`: Database logic, Embedding singleton, and LLM manager.
- `scripts/`: Ingestion pipeline for file processing.
- `web/`: Streamlit frontend components and styles.
- `data/`: Folder for technical data files.
- `Dockerfile` & `docker-compose.yml`: For easy deployment.

---

**Developed for Rose Blanche Group | KnowledgeQuest RAG Module**
**Made for AI Night Challenge by CTRL+S**
