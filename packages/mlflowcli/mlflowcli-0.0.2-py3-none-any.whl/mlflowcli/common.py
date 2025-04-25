import hashlib
import urllib.request
from pathlib import Path
from typing import List


def checksum_alg(file_path, algorithm):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        return hash_remote_file(file_path, algorithm)
    else:
        return hash_local_file(file_path, algorithm)


def checksum_folder_alg(dir_name: Path, algorithm: str, file_paths: List[str] = None):
    if file_paths is None:
        paths = dir_name.rglob("*")
    else:
        paths = [Path(file_path) for file_path in file_paths]
    checksum_values = ""
    for path_name in paths:
        if path_name.is_file():
            checksum_values += checksum_alg(str(path_name), algorithm)
        else:
            print(f"Skipping checksum file: {path_name}")

    return checksum_values


def get_hash_func(algorithm):
    if algorithm == "md5":
        hash_func = hashlib.md5()
    elif algorithm == "sha1":
        hash_func = hashlib.sha1()
    elif algorithm == "sha256":
        hash_func = hashlib.sha256()
    elif algorithm == "sha384":
        hash_func = hashlib.sha384()
    elif algorithm == "sha512":
        hash_func = hashlib.sha512()
    else:
        raise ValueError(f"Invalid algorithm: {algorithm}")
    return hash_func


def hash_local_file(file_path, algorithm="md5"):
    file_path = Path(file_path)
    hash_func = get_hash_func(algorithm=algorithm)

    with file_path.open("rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def hash_remote_file(url, algorithm="md5"):
    max_file_size = 100 * 1024 * 1024  # 100 MB
    hash_func = get_hash_func(algorithm=algorithm)

    with urllib.request.urlopen(url) as response:
        total_read = 0
        while True:
            data = response.read(4096)
            if not data:
                break
            total_read += len(data)
            hash_func.update(data)
            if total_read > max_file_size:
                break

    return hash_func.hexdigest()
