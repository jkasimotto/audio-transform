import subprocess
import os
import tempfile


# def move_moov_atom_to_start(audio_bytes):
#     """
#     This function takes an audio byte stream as input, processes it using FFmpeg to move the 'moov' atom
#     to the start of the file, and returns the processed audio byte stream.

#     :param audio_bytes: The input audio byte stream
#     :return: The processed audio byte stream
#     """
#     # Create a temporary file
#     temp_file = tempfile.NamedTemporaryFile(delete=False)
#     temp_file.close()

#     # Define the FFmpeg command to remux the file:
#     # -i pipe:0: Use stdin (pipe:0) as the input source
#     # -c copy: Use the "copy" codec to avoid re-encoding the audio stream
#     # -f m4a: Force the output format to M4A
#     # -movflags +faststart: Move the 'moov' atom to the start of the file for faster playback
#     # pipe:1: Use stdout (pipe:1) as the output destination
#     command = [
#         'ffmpeg', '-i', 'pipe:0', '-c', 'copy', '-f', 'mp4',
#         '-movflags', '+faststart', 'pipe:1'
#     ]

#     # Execute the FFmpeg command using subprocess:
#     # input: Pass the input audio byte stream to stdin
#     # stdout: Capture the processed audio byte stream from stdout
#     # stderr: Capture FFmpeg's error messages, if any
#     # check: Raise an exception if the subprocess exits with a non-zero status
#     try:
#         result = subprocess.run(
#             command, input=audio_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
#         )
#     except subprocess.CalledProcessError as e:
#         print("Error running ffmpeg command:", e.stderr.decode('utf-8'))
#         print("Command:", e.cmd)
#         print("Return code:", e.returncode)
#         print("Output:", e.output.decode('utf-8'))
#         if e.returncode != 0:
#             print("Error running ffmpeg command:", e.stderr.decode('utf-8'))
#         raise e

#     # Get the processed audio byte stream from the result's stdout
#     return result.stdout


def move_moov_atom_to_start(audio_bytes):

    # Create a temporary file using the tempfile module. This file will be used to store the output from FFmpeg.
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    # Close the temporary file to release any resources (file handles) associated with it.
    # We'll later read and write to the file using different file objects, so we don't need the original file object open.
    temp_file.close()

    # Modify the FFmpeg command to use the temporary file as the output destination.
    command = ['ffmpeg', '-y', '-i', 'pipe:0', '-c', 'copy', '-f',
               'mp4', '-movflags', '+faststart', temp_file.name]

    # Run the FFmpeg command using subprocess.Popen, which takes the command as a list of arguments.
    # We provide the input data through the stdin parameter by using subprocess.PIPE.
    try:
        process = subprocess.Popen(
            command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # audio_bytes is the input data in bytes format
        _, stderr_data = process.communicate(input=audio_bytes)
        process.wait()
    except Exception as e:
        print("Error running the ffmpeg command:", e)
    else:
        # Check if the command was successful by examining the return code (0 means success).
        if process.returncode != 0:
            print("Error running ffmpeg command:", stderr_data.decode('utf-8'))
        else:
            # If the command was successful, read the contents of the temporary file.
            with open(temp_file.name, "rb") as output_data:
                output_bytes = output_data.read()
                return output_bytes

    # Delete the temporary file using os.unlink, which removes the file from the filesystem.
    os.unlink(temp_file.name)
