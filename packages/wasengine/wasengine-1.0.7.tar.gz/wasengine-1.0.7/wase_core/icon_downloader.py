import os
import zipfile
import hashlib
import requests

# Force BASE_PATH to WAStudio's root directory
BASE_PATH = os.path.join(os.getcwd(), 'wase_data')
zip_path = os.path.join(BASE_PATH, 'icons.zip')
extract_path = os.path.join(BASE_PATH, 'icons')
filenames_file = os.path.join(BASE_PATH, 'filenames.txt')

KNOWN_FILENAMES_HASH = "dd6ef9b97ba3ea2b17d3c32924a0db87"

def md5_file(filepath):
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def generate_filenames_file():
    with open(filenames_file, 'w', encoding='utf-8') as f:
        for root, dirs, files in os.walk(extract_path):
            for name in sorted(files):
                rel_path = os.path.relpath(os.path.join(root, name), extract_path)
                f.write(rel_path + '\n')

def download_icons():
    os.makedirs(BASE_PATH, exist_ok=True)
    print("Downloading icons.zip from GitHub...")
    url = 'https://github.com/WAStudios/WASEngine/releases/download/icons/icons.zip'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete.")
    else:
        raise Exception(f"Failed to download icons.zip, status code: {response.status_code}")

def get_icons():
    if not os.path.exists(extract_path) or not os.path.exists(filenames_file):
        print("Missing icons or filenames.txt, downloading...")
        if not os.path.exists(zip_path):
            download_icons()
        print("Extracting icons.zip...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        generate_filenames_file()
        print("Generated filenames.txt")
    else:
        print("Verifying filenames.txt integrity...")
        current_hash = md5_file(filenames_file)
        print(f"Filenames MD5: {current_hash}")
        if current_hash == KNOWN_FILENAMES_HASH:
            print("File structure is valid.")
        else:
            print("File structure invalid. Re-downloading icons.")
            os.remove(zip_path)
            os.remove(filenames_file)
            for root, dirs, files in os.walk(extract_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(extract_path)
            return get_icons()

    return extract_path
