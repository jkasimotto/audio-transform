import os
import subprocess
import tempfile
from io import BytesIO

import ffmpeg
from pydub import AudioSegment


def convert_audio(request):
    # Get the bytes and file extension from the request
    audio_bytes = request.get_data()
    file_extension = request.headers.get('file-extension', None)
    # Move the moov atom to the start of the file
    audio_bytes = move_moov_atom_to_start(audio_bytes)
    return audio_bytes


def move_moov_atom_to_start(audio_bytes):

    # Create a temporary input file
    with tempfile.NamedTemporaryFile(suffix=".m4a") as input_file:
        # Write the audio bytes to the temporary file
        input_file.write(audio_bytes)
        # Flush the buffer to the file
        input_file.flush()

        # Define the command to remux the file
        command = ['ffmpeg', '-i', input_file.name, '-c', 'copy', '-f', 'm4a', '-movflags', '+faststart', 'output.m4a']
        
        # Execute the command using subprocess
        subprocess.run(command, check=True)

        # Read the output file
        with open("output.m4a", "rb") as output_file:
            output_bytes = output_file.read()

    # Delete the output file if it exists
    os.remove("output.m4a")

    return output_bytes