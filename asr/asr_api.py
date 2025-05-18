from fastapi import FastAPI, UploadFile, File
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from pydub import AudioSegment
import soundfile as sf
import torch
import os

# Initialize FastAPI app
app = FastAPI()

# Load model and processor once when app starts
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")

# Routing decorators
@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/asr")   # ASR inference endpoint
async def transcribe(file: UploadFile = File(...)):
    # Save uploaded mp3 to disk
    input_temp = "input.mp3"
    with open(input_temp, "wb") as f:
        f.write(await file.read())

    # Convert to 16kHz WAV using pydub
    audio = AudioSegment.from_file(input_temp)
    audio = audio.set_frame_rate(16000).set_channels(1)
    wav_path = "temp.wav"
    audio.export(wav_path, format="wav")

    # Load audio into array
    speech, _ = sf.read(wav_path)

    # Transcribe with wav2vec2
    inputs = processor(speech, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]

    # Get duration in seconds
    duration_sec = len(audio) / 1000.0

    # Clean up temp files
    os.remove(input_temp)
    os.remove(wav_path)

    return {
        "transcription": transcription,
        "duration": f"{duration_sec:.1f}"
    }
