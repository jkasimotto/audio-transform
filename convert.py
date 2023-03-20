import subprocess
import tempfile

def move_moov_atom_to_start(audio_bytes):
    with tempfile.NamedTemporaryFile(delete=True, suffix='mp4') as input_temp_file, \
         tempfile.NamedTemporaryFile(delete=True, suffix='mp4') as output_temp_file:

        # Save the input data to a temporary file
        input_temp_file.write(audio_bytes)
        input_temp_file.flush()

        # Modify the FFmpeg command to use the temporary input and output files
        command = ['ffmpeg', '-y', '-i', input_temp_file.name, '-c', 'copy', '-f', 'mp4', '-movflags', '+faststart', output_temp_file.name]

        # Run the FFmpeg command using subprocess.Popen, which takes the command as a list of arguments.
        try:
            process = subprocess.Popen(command, stderr=subprocess.PIPE)
            _, stderr_data = process.communicate()
            process.wait()
        except Exception as e:
            print("Error running the ffmpeg command:", e)
        else:
            # Check if the command was successful by examining the return code (0 means success).
            if process.returncode != 0:
                print("Error running ffmpeg command:", stderr_data.decode('utf-8'))
            else:
                # If the command was successful, read the contents of the temporary output file.
                with open(output_temp_file.name, "rb") as output_data:
                    output_bytes = output_data.read()
                return output_bytes

    return None
