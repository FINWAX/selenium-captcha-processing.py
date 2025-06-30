import base64

import requests


def download_audio(link_or_data, mp3_file):
    """
    Download audio content from a link or data URI and save it to a file.
    :param link_or_data: The URL or data URI of the audio content.
    :param mp3_file: The file path to save the audio content.
    """
    if link_or_data.startswith("data:audio"):
        base64_data = link_or_data.split(",")[1]
        audio_content = base64.b64decode(base64_data)
    else:
        audio_download = requests.get(url=link_or_data, allow_redirects=True)
        audio_content = audio_download.content

    with open(mp3_file, 'wb') as f:
        f.write(audio_content)
        f.close()
