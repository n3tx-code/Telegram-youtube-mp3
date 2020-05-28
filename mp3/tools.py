import random
import string
import youtube_dl

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from youtube_dl.utils import UnsupportedError, DownloadError

def videoDurationIsLessThen10Min(url):
    ydl = youtube_dl.YoutubeDL()
    with ydl:
        result = ydl.extract_info(
            url,
            download=False  # We just want to extract the info
        )

    if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
    else:
        # Just a video
        video = result

    if video['duration'] < 600:
        return True

    return False


def generateRandomFolderName():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


def isCorrectYoutubeUrl(url):
    val = URLValidator()
    try:
        val(url)

        ydl = youtube_dl.YoutubeDL()
        with ydl:
            try:
                ydl.extract_info(
                    url,
                    download=False)
            except UnsupportedError as e:
                return False
            except DownloadError as e:
                return False
        return True
    except ValidationError as e:
        return False
