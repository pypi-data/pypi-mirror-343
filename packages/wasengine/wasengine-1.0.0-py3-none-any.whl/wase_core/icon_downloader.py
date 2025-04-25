import gdown
import zipfile
import os
import hashlib
import shutil
import threading
import time

KNOWN_GOOD_HASH = 'a53c748e04baf70f9bbdae4f04186adc'  # Replace with actual hash

def md5_dir(directory):
    hash_md5 = hashlib.md5()
    for root, dirs, files in os.walk(directory):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_icons():
    url = 'https://drive.google.com/uc?id=1hzbHyF8qGSA53fYnl8H7UMNUrmFC49KU'
    zip_path = '../wase_data/icons.zip'
    extract_path = '../wase_data/icons/'

    os.makedirs('../wase_data', exist_ok=True)

    if os.path.exists(extract_path):
        print("Found existing icons folder. Verifying integrity...")

        # Start async dot printing
        running = True
        def dot_printer():
            while running:
                print("... ", end="", flush=True)
                time.sleep(1.5)

        thread = threading.Thread(target=dot_printer)
        thread.start()

        # Time the hashing
        start_time = time.time()
        current_hash = md5_dir(extract_path)
        elapsed_time = (time.time() - start_time) * 1000  # ms
        running = False
        thread.join()
        print()  # Move to next line after dots

        if current_hash == KNOWN_GOOD_HASH:
            print(f"Icons folder is valid. No need to download. (Checked in {elapsed_time:.0f} ms)")
            return extract_path
        else:
            print("Icons folder hash mismatch. Cleaning up...")
            shutil.rmtree(extract_path)
            if os.path.exists(zip_path):
                os.remove(zip_path)

    if os.path.exists(zip_path):
        print("Found existing icons.zip. Extracting...")
    else:
        print("Downloading icons.zip...")
        downloaded = gdown.download(url, zip_path, quiet=False)
        if not downloaded or not os.path.exists(zip_path):
            print("Download failed.")
            return None

    print("Extracting icons.zip...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    print(f"Icons extracted to {extract_path}")

    os.remove(zip_path)
    print("Cleaned up icons.zip")

    return extract_path
