import sys
import time
import requests
from enimation.loading import CustomLoading

def progress_bar_animation(stop_event, text="Downloading", total_size=100):
    """
    Custom progress bar animation for image downloading.
    """
    def update_progress_bar(progress, total):
        bar_length = 40
        block = int(bar_length * progress / total)
        sys.stdout.write(f'\r{text}: [{"#" * block}{"-" * (bar_length - block)}] {progress}/{total} KB')
        sys.stdout.flush()

    downloaded = 0
    while not stop_event.is_set() and downloaded < total_size:
        update_progress_bar(downloaded, total_size)
        time.sleep(0.1)  # This would be updated with actual download progress
        downloaded += 5  # Increment progress for demonstration purposes

    # Complete the bar when finished
    if downloaded >= total_size:
        update_progress_bar(total_size, total_size)
        sys.stdout.write("\nDownload complete!\n")

def download_image(url, filepath):
    """
    Download an image with a custom loading progress bar.
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0)) // 1024  # KB

    loader = CustomLoading(custom=lambda stop_event: progress_bar_animation(stop_event, total_size=total_size))
    loader.start()

    with open(filepath, 'wb') as file:
        downloaded = 0
        for data in response.iter_content(1024):  # 1 KB at a time
            file.write(data)
            downloaded += 1

    loader.stop()
    print("\nImage downloaded successfully!")

if __name__ == "__main__":
    # Test with an example image URL
    download_image("https://i.ibb.co/pngXvt1/download-4.jpg", "image.jpg")
