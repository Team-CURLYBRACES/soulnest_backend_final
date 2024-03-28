from users.models import User
from django.http import HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json

url = 'https://663a-124-43-246-34.ngrok-free.app/predict'


@csrf_exempt
def index(request):
    users = User.objects.all()
    for user in users:
        if user.chats:
            messages = ""
        for i in range(len(user.chats)):
            if user.chats[0].is_stress_checked == True:
                    messages += (user.chats[0].text + '.')
                    user.chats[0].is_stress_checked == True
                    data = {"response":messages}
        response = requests.post(url, json={"response":messages})
        print(messages)
        data = response.json()
        print(data)
        percentage = data['stress_percentage']
        user.stress_level.append(percentage)
        user.save()