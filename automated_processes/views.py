from users.models import User
from django.http import HttpResponse
import requests

url = 'http://127.0.0.1:8001/predict'

def index(request):
    users = User.objects.all()
    for user in users:
        if user.chats:
            messages = ""
            for i in range(len(user.chats)):
                if user.chats[i].is_stress_checked == False:
                    messages += (user.chats[i].text + '.')
                    user.chats[i].is_stress_checked == True
                    print(messages)
                response = requests.post(url, json={"response": messages})
                data = response.json()
                percentage = data['stress_percentage']
                user.stress_level.append(percentage)
                user.save()