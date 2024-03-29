from users.models import User
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json

url = 'https://9a76-2402-d000-a400-3124-2c1a-67c4-4303-9cff.ngrok-free.app/predict'


@csrf_exempt
def index(request):
    users = User.objects.all()
    for user in users:
        if user.chats:
            messages = ""
        for i in range(len(user.chats)):
            if user.chats[i].is_stress_checked == False:
                    messages += (user.chats[i].text + '.')
                    user.chats[i].is_stress_checked == True
                    data = {"response":messages}
        response = requests.post(url, json={"response":messages})
        print(response)
        print(messages)
        data = response.json()
        print(data)
        percentage = data['stress_percentage']
        print('here')
        user.stress_level.append(percentage)
        user.save()
    return JsonResponse({"message":"Process carried out successfully"}, status=201)