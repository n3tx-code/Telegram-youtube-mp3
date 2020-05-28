from __future__ import unicode_literals
import os
import shutil

import requests
import youtube_dl

from mp3.tools import videoDurationIsLessThen10Min, generateRandomFolderName, isCorrectYoutubeUrl

folder = generateRandomFolderName()


def downloadMp3(url, chatId):
    if isCorrectYoutubeUrl(url) is False:
        requests.post(
            'https://api.telegram.org/<YOUR_TELEGRAM_BOT_API>/sendMessage',
            data={'chat_id': chatId, "text": "Url non valide"})
    else:
        if videoDurationIsLessThen10Min(url):
            class MyLogger(object):
                def debug(self, msg):
                    pass

                def warning(self, msg):
                    pass

                def error(self, msg):
                    requests.post(
                        'https://api.telegram.org/<YOUR_TELEGRAM_BOT_API>/sendMessage',
                        data={'chat_id': chatId, "text": "Une erreur est survenue"})

            def my_hook(d):
                if d['status'] == 'finished':
                    print('Done downloading, now converting ...')

            ydl_opts = {
                'format': 'bestaudio/best',
                'writethumbnail': True,
                'outtmpl': 'static/dl/' + folder + '/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                    {'key': 'EmbedThumbnail'},
                    {'key': 'FFmpegMetadata'},
                ],
                'logger': MyLogger(),
                'progress_hooks': [my_hook],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            mp3_file_path = 'static/dl/' + folder + "/" + os.listdir("static/dl/" + folder)[0]

            audio = open(mp3_file_path, 'rb')

            r = requests.post('https://api.telegram.org/<YOUR_TELEGRAM_BOT_API>/sendAudio',
                              data={'chat_id': chatId}, files={"audio": audio})
            if r.status_code == 200:
                shutil.rmtree('static/dl/' + folder)

        else:
            requests.post(
                'https://api.telegram.org/<YOUR_TELEGRAM_BOT_API>/sendMessage',
                data={'chat_id': chatId, "text": "Vidéo trop longue (plus de 10mins)"})
