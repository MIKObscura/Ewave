from pathlib import Path

EXTENSIONS = ["mp3", "flac", "ogg"] # will be expanded in the future

def get_all_files(*base_dirs):
    """
    searches recursively in all the dirs for files
    """
    files = []
    for dir in base_dirs:
        for file in Path(dir).rglob("*"):
            files.append(file) if not file.is_dir() else True
    return files

def filter_files(filelist):
    """
    filter the files to keep audio files only
    """
    return list(filter(lambda f: f.name.split(".")[len(f.name.split(".")) - 1] in EXTENSIONS, filelist))
