import os
import hashlib


def get_file_hash(path):
    h = hashlib.md5()

    with open(path, "rb") as file:
        while True:
            chunk = file.read(4096)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_filename(path):
    return os.path.basename(path)