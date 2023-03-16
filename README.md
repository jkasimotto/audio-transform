# audio-transform
Transformations of audio files using ffmpeg for ETL in Animus.

Transformations:
1. Move the 'moov' atom containing metadata about the audio to the beginning of the bytestream. This allows whisper to transcribe it and for faster playback.


