import audio_metadata

def get_metadata(path):
    return audio_metadata.load(path)

