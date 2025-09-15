from pytube import YouTube
import os

# path
link_path = "../data/links"
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

with open(link_path, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    try:
        yt = YouTube(url)  #: Create a YouTube object
        title = yt.title.replace(" ", "_").replace("/", "_")  #: title of the video
        print(f"Downloading: {title}")

        # downloading audio file only
        audio_stream = yt.streams.filter(only_audio=True).first()
        download_path = audio_stream.download(output_path="downloads", filename=f"{title}.mp4")

    except Exception as e:
        print(f"Failed for {url}: {e}")

