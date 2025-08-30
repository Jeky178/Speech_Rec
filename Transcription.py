import time
import requests


from SPEECH_RECOGNITION_3.secret_key import API_KEY_ASSEMBLYAI
filename = "new_record.wav"
api_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
headers = {"authorization": API_KEY_ASSEMBLYAI}

# upload our local audio file to assemblyai  with a post request including  the headers for authentication for the audio url
def upload(filename):
    def read_file(filename, chunk_size = 5242880):
        with open(filename, "rb") as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    request_response = requests.post(api_endpoint, headers =headers, data=read_file(filename))
    audio_url = request_response.json()["upload_url"]
    return audio_url


# transcript
def transcribe(audio_url):
    transcript_request = {"audio_url":audio_url}
    transcript_response = requests.post(transcript_endpoint,json=transcript_request, headers=headers)
    job_id = transcript_response.json()["id"]
    return job_id

# poll
def poll(transcription_id):
    poll_endpoint = transcript_endpoint + "/" + transcription_id
    poll_response =requests.get(poll_endpoint, headers=headers)
    return poll_response.json()





def get_transcription_result_url(audio_url):
    transcription_id = transcribe(audio_url)
    while True:
        data = poll(transcription_id)
        if data["status"] == "completed":
            return data, None
        elif data["status"] == "error":
            return data, data["error"]

        print("Waiting for 30 seconds....")
        time.sleep(30)

def save_transcript(audio_url):
    data, error = get_transcription_result_url(audio_url)
    if data:
        text_filename = filename + ".txt"
        with open(text_filename, "w") as f:
            f.write(data["text"])
        print("Transcription saved")

    elif error:
        print("Error", error)

audio_url = upload(filename)
save_transcript(audio_url)