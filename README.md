# HTX xData Technical Test (AIE) – Speech-to-Text Pipeline with Search UI

This project implements a full-stack AI pipeline featuring:
- Automatic Speech Recognition (ASR) using `wav2vec2`
- Transcription of Common Voice mp3 files
- Elasticsearch backend indexing
- React-based Search UI frontend
- Containerized deployment (optional)

---

## Repository Structure
htx-asr/
│
├── asr/ # ASR microservice with FastAPI
│ ├── asr_api.py
│ └── Dockerfile
│
├── elastic-backend/ # Elasticsearch setup and indexer
│ ├── docker-compose.yml
│ └── cv-index.py
│
├── search-ui/ # React-based Search UI
│ └── app/ # Created via Create React App
│ ├── src/
│ ├── public/
│ └── Dockerfile # Optional for deployment
│
├── cv-decode.py # Transcribe Common Voice mp3s via ASR API
├── requirements.txt
├── .gitignore
├── design.pdf # Deployment architecture (draw.io)
└── essay.pdf # Monitoring & drift detection strategy


---

## API Endpoints

### `/ping` — Health check
```http
GET http://<your-server-ip>:8001/ping
```
**Response:**
```json
{ "message": "pong" }
```

---

### `/asr` — Transcribe mp3 audio
```http
POST http://<your-server-ip>:8001/asr
Content-Type: multipart/form-data
Form field: file (mp3)
```

**Example using cURL:**
```bash
curl -F "file=@sample.mp3" http://<your-server-ip>:8001/asr
```

**Response:**
```json
{
  "transcription": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
  "duration": "4.5"
}
```

---

## Batch Transcription

Use `cv-decode.py` to automatically process and transcribe a dataset of mp3 files.

```bash
python cv-decode.py
```

- Calls the ASR API on each file
- Appends the result to `generated_text` column in `cv-valid-dev.csv`

---

## Search Interface

Access the search UI at:

```
http://<your-server-ip>:3000
```

### Searchable Fields:
- Transcribed Text
- Duration (e.g., 0–5s, 5–10s, 10+s)
- Speaker Age
- Gender
- Accent

Use the search bar and filters in the sidebar to refine your results.

---

## Proposed Architecture

The system consists of 3 main services:

```
[User] ──────────────▶ [Search UI Web App - port 3000]
           ▲                     │
           │                     ▼
      [Transcription Script] ─▶ [Elasticsearch - port 9200]
           │                     ▲
           ▼                     │
   [ASR Inference API - port 8001]  ◀─── mp3 uploads
```

### Components:
- **ASR API** (FastAPI + HuggingFace Transformers): Accepts audio and returns transcription + duration
- **Elasticsearch** (cv-transcriptions index): Stores all transcribed records with metadata
- **Search UI** (React + Elastic Search UI): Provides frontend for filtering and searching

---

## System Requirements

- Docker + Docker Compose (optional for containerized deployment)
- Python 3.8+ for API and transcription scripts
- Node 16+ for Search UI (if running locally)

---

## Notes

- All audio input must be mp3 format, 16kHz sampling rate is automatically enforced
- Transcription model is pre-trained and ready for inference
- Temporary audio files are automatically deleted after processing

