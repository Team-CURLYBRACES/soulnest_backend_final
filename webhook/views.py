from django.shortcuts import render
from django.http import JsonResponse, HttpRequest, HttpResponse
import json
from openai import OpenAI
import openai
from django.views.decorators.csrf import csrf_exempt


convo = [{"role": "system", "content": "The following is a conversation with a therapist and a user. The therapist uses compassionate listening to have helpful and meaningful conversations with users. The therapist is empathic and friendly. The therapists's objective is to make the user feel better by feeling heard. With each response, the therapist offers follow-up questions to encourage openness and tries to continue the conversation in a natural way."}]

@csrf_exempt
def webhook(request: HttpRequest):
    if(request.method == 'POST'):
        req_data = json.loads(request.body)
        query_result = req_data.get('queryResult')
        query = query_result.get('queryText') 

        if(query_result.get('action') == 'input.unknown'):
            convo.append({"role" : "user", "content" : query})
            response = ask_gpt(query)
            convo.append({"role" : "assistant", "content" : response})
            print(response)
            reply = {
                "fulfillmentText" : response,
                "source" : "webhook data" 
            }
            return JsonResponse(reply) 
    return HttpResponse('hyyy')

def ask_gpt(prompt):

    openai.api_key = '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'
    client = OpenAI()

    completion = client.chat.completions.create(
        model= 'ft:gpt-3.5-turbo-1106:curlybraces:mentalhc:91vJAXms',
        messages= convo
    )
    return completion.choices[0].message.content