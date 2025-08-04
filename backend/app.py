import requests
import json
import base64
import os

from flask import Flask, request, send_from_directory, url_for, Blueprint


app = Flask(__name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/audio/<path:path>')
def send_audio(path):
    return send_from_directory('audio', path)


@api_bp.post('/tts')
def tts():
    VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
    API_KEY = os.getenv('ELEVENLABS_API_KEY')

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"

    headers = {
        "Content-Type": "application/json",
        "xi-api-key": API_KEY
    }

    text = request.data.decode('utf-8')

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
    )

    if response.status_code != 200:
        print(f"Error encountered, status: {response.status_code}, "
              f"content: {response.text}")
        quit()

    # convert the response which contains bytes into a JSON string from utf-8 encoding
    json_string = response.content.decode("utf-8")

    # parse the JSON string and load the data as a dictionary
    response_dict = json.loads(json_string)

    # the "audio_base64" entry in the dictionary contains the audio as a base64 encoded string,
    # we need to decode it into bytes in order to save the audio as a file
    audio_bytes = base64.b64decode(response_dict["audio_base64"])

    filename = f'audio/output_{hash(text)}.mp3'
    with open(filename, 'wb') as f:
        f.write(audio_bytes)

    # the 'alignment' entry contains the mapping between input characters and their timestamps
    meta_data = response_dict['alignment']

    word = ''
    result = {
        'start_time': [],
        'end_time': [],
        'words': []
    }
    for i, char in enumerate(meta_data['characters']):
        if len(word) == 0:
            result['start_time'].append(
                meta_data['character_start_times_seconds'][i]
            )
        if char in ' \n':
            result['words'].append(word)
            word = ''
            result['end_time'].append(meta_data['character_end_times_seconds'][i-1])
        else:
            word += char
            if i + 1 == len(meta_data['characters']):
                result['words'].append(word)
                result['end_time'].append(meta_data['character_end_times_seconds'][i])

    audio_path = filename.replace('audio/', '')
    return {
        'adjusted_alignment': result,
        'audioUrl': url_for('api.send_audio', path=audio_path, _external=True)
    }


app.register_blueprint(api_bp)

