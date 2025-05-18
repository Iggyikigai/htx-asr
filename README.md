# HTX xData Technical Test (AIE) – Speech-to-Text Pipeline with Search UI

## Live Deployment  
Access the deployed application here:  
**[http://20.2.138.15:3000](http://20.2.138.15:3000)**

## Branches  
- `main`: Source code for ASR microservice, indexing, and UI  
- `deployment`: Contains deployment instructions, Dockerfiles, and configuration details

---

## 1. Getting Started

### Prerequisites
- Python 3.8+  
- Node.js 16+ (for local Search UI)  
- Docker + Docker Compose (for full containerized setup)

### Installation (Local, non-Docker)
```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend setup
cd search-ui/app
npm install
npm start
```

---

## 2. ASR Microservice

### Dataset  
We use Mozilla’s **Common Voice** dataset for speech-to-text tasks.  
🔗 [https://commonvoice.mozilla.org/en/datasets](https://commonvoice.mozilla.org/en/datasets)

### File: `asr/asr_api.py`  
- Implements an ASR microservice using FastAPI and HuggingFace `wav2vec2`
- Accepts `.mp3` uploads and returns transcription and duration

### Endpoints
- **Health Check**  
  `GET /ping` → `{ "message": "pong" }`  
- **Transcription**  
  `POST /asr`  
  Content-Type: `multipart/form-data`  
  Field: `file` (mp3)

Example:
```bash
curl -F "file=@sample.mp3" http://<your-server-ip>:8001/asr
```

Response:
```json
{
  "transcription": "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG",
  "duration": "4.5"
}
```

### Batch Processing: `cv-decode.py`
- Transcribes multiple `.mp3` files and updates the CSV with results under `generated_text`

---

## 3. Elastic-Backend

### Folder: `elastic-backend/`  
- `docker-compose.yml`: Multi-node Elasticsearch + Kibana setup  
- `cv-index.py`:  
  - Indexes transcriptions and metadata into the `cv-transcriptions` index  
  - Accepts cleaned `.csv` input

### Searchable Fields
- `generated_text` (transcription)  
- `duration`  
- `gender`  
- `age`  
- `accent`

---

## 4. Search-UI

### Folder: `search-ui/app/`  
- React app created using Create React App  
- Integrates `@elastic/react-search-ui` for real-time query and filtering

### Access
Deployed frontend (via Nginx):  
**[http://20.2.138.15:3000](http://20.2.138.15:3000)**

### Features
- Full-text search on transcriptions  
- Filter by speaker metadata  
- Responsive interface with Elastic UI components

---

## Repository Structure

- `asr/`
  - `asr_api.py`
  - `Dockerfile`
- `elastic-backend/`
  - `docker-compose.yml`
  - `cv-index.py`
- `search-ui/`
  - `app/`
    - `src/`
    - `public/`
    - `Dockerfile`
- `cv-decode.py`
- `requirements.txt`
- `.gitignore`
- `design.pdf`
- `essay.pdf`
