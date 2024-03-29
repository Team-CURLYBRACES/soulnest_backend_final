from users.models import User
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import json

url = 'http://188.166.196.163:8001/predict/'


@csrf_exempt
def index(request):
    users = User.objects.all()
    for user in users:
        if user.chats:
            messages = ""
        for i in range(len(user.chats)):
            if user.chats[i].is_stress_checked == True:
                    messages += (user.chats[i].text + '.')
                    user.chats[i].is_stress_checked == True
                    data = {"response":messages}
        response = requests.post(url, json={"response":messages})
        data = response.json()
        percentage = data['stress_percentage']
        user.stress_level.append(percentage)
        user.save()
    return JsonResponse({"message":"Process carried out successfully"}, status=201)