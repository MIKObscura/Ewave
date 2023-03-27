from pathlib import Path

EXTENSIONS = ["mp3", "flac", "ogg"]

def get_all_files(*base_dirs):
    files = []
    for dir in base_dirs:
        for file in Path(dir).rglob("*"):
            files.append(file) if not file.is_dir() else True
    return files

def filter_files(filelist):
    return list(filter(lambda f: f.name.split(".")[len(f.name.split(".")) - 1] in EXTENSIONS, filelist))
