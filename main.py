import os
from flask import Flask, request
from convert import move_moov_atom_to_start

app = Flask(__name__)


# main.py

@app.route('/', methods=['POST'])
def handle_request():
    # Get the bytes and file extension from the request
    audio_bytes = request.get_data()
    file_extension = request.headers.get('file-extension', None)

    # Move the moov atom to the start of the file
    audio_bytes = move_moov_atom_to_start(audio_bytes)

    return audio_bytes, 200, {'Content-Type': 'audio/m4a'}



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

