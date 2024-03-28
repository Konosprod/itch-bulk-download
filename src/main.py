import os
import pathlib
from collections import deque

import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

urls = []
OUTPUT_DIR = pathlib.Path(os.getenv('OUTPUT_DIR'))
API_KEY = os.getenv('API_KEY')
CSRF_TOKEN = os.getenv('CSRF_TOKEN')

file_source = open(pathlib.Path(__file__).parent.parent / 'links.txt', 'r+')
urls = deque(file_source.readlines())

while urls:
    url = urls.popleft()
    url = url.strip()
    response = requests.get(url+"data.json", headers=headers).json()
    id = response['id']
    response = requests.get(
        f"https://itch.io/api/1/{API_KEY}/game/{id}/uploads").json()
    for upload in response['uploads']:
        if upload['p_windows']:
            fileid = upload['id']
            filename = upload['filename']
            newurl = f"{url}file/{fileid}?source=game_download"
            response = requests.post(
                newurl, {"csrf_token": ""})
            download_url = response.json()['url']

            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            print("Downloading", filename, "from", url)
            with open(OUTPUT_DIR / filename, 'wb') as file, tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=4096) as bar:
                if (total_size == 0):
                    file.write(response.content)
                else:
                    for data in response.iter_content(chunk_size=4096):
                        size = file.write(data)
                        bar.update(size)

    file_source.truncate(0)
    file_source.writelines([str(element)+'\n' for element in urls])
