import os
from flask import Flask, request
from convert import convert_audio

app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_request():
    output_bytes = convert_audio(request)
    return output_bytes, 200, {'Content-Type': 'audio/m4a'}


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
