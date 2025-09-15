import os

links_file = "../data/links"
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

with open(links_file, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

for url in urls:
    os.system(f'yt-dlp -x --audio-format mp3 -o "{download_dir}/%(title)s.%(ext)s" {url}')
