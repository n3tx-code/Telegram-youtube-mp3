import json
import requests
from django.http import Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from mp3.downloadMp3 import downloadMp3


@csrf_exempt
def messageFromTelegram(request):
    if request.method == 'POST':

        try:
            telegramMsg = json.loads(request.body)
            chatId = telegramMsg['message']['from']['id']
            urlSended = telegramMsg['message']['text']
            downloadMp3(urlSended, chatId)
        except:
            try:
                telegramMsg = json.loads(request.body)
                chatId = telegramMsg['message']['from']['id']
                requests.post(
                    'https://api.telegram.org/<YOUR_TELEGRAM_BOT_API>/sendMessage',
                    data={'chat_id': chatId, "text": "Une erreur est survenue"})
            except:
                raise Http404("What are you doing your stupid bot ?")

        return HttpResponse("""
               <a href="http://t.me/YoutubeMp3TelegramBot">http://t.me/YoutubeMp3TelegramBot</a>
           """)
    else:
        return HttpResponse("""
                       <a href="http://t.me/YoutubeMp3TelegramBot">http://t.me/YoutubeMp3TelegramBot</a>
                   """)
