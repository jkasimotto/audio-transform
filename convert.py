import subprocess


def move_moov_atom_to_start(audio_bytes):
    """
    This function takes an audio byte stream as input, processes it using FFmpeg to move the 'moov' atom
    to the start of the file, and returns the processed audio byte stream.

    :param audio_bytes: The input audio byte stream
    :return: The processed audio byte stream
    """

    # Define the FFmpeg command to remux the file:
    # -i pipe:0: Use stdin (pipe:0) as the input source
    # -c copy: Use the "copy" codec to avoid re-encoding the audio stream
    # -f m4a: Force the output format to M4A
    # -movflags +faststart: Move the 'moov' atom to the start of the file for faster playback
    # pipe:1: Use stdout (pipe:1) as the output destination
    command = [
        'ffmpeg', '-i', 'pipe:0', '-c', 'copy', '-f', 'mp4',
        '-movflags', '+faststart', 'pipe:1'
    ]

    # Execute the FFmpeg command using subprocess:
    # input: Pass the input audio byte stream to stdin
    # stdout: Capture the processed audio byte stream from stdout
    # stderr: Capture FFmpeg's error messages, if any
    # check: Raise an exception if the subprocess exits with a non-zero status
    try:
        result = subprocess.run(
            command, input=audio_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error running ffmpeg command:", e.stderr.decode('utf-8'))
        print("Command:", e.cmd)
        print("Return code:", e.returncode)
        print("Output:", e.output.decode('utf-8'))
        if e.returncode != 0:
            print("Error running ffmpeg command:", e.stderr.decode('utf-8'))
        raise e

    # Get the processed audio byte stream from the result's stdout
    return result.stdout
