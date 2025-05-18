#This file calls API to localhost:8001
import os
import requests
import pandas as pd

# Correct CSV and audio folder paths based on your structure
CSV_PATH = "../common_voice/cv-valid-dev/cv-valid-dev.csv"
AUDIO_FOLDER = "../common_voice/cv-valid-dev/cv-valid-dev"

ASR_ENDPOINT = "http://localhost:8001/asr"

# Load the CSV file
df = pd.read_csv(CSV_PATH)
transcriptions = []

for idx, row in df.iterrows():
    try:
        # The 'filename' column already includes the correct filename
        mp3_filename = os.path.basename(row["filename"])
        file_path = os.path.join(AUDIO_FOLDER, mp3_filename)

        with open(file_path, "rb") as f:
            response = requests.post(ASR_ENDPOINT, files={"file": f})
            if response.status_code == 200:
                result = response.json()
                text = result.get("transcription", "")
            else:
                print(f"API Error for {file_path}: HTTP {response.status_code}")
                text = ""
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        text = ""

    transcriptions.append(text)

# Append the transcriptions to the dataframe
df["generated_text"] = transcriptions

# Save updated CSV
df.to_csv(CSV_PATH, index=False)
print(f"Transcription completed: {sum(bool(t) for t in transcriptions)}/{len(transcriptions)} files transcribed.")