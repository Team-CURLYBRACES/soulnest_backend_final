from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def predict_stress_percentage(request: HttpRequest):
    if request.method == 'POST':
        # Receive user response from user database
        user_response = request.POST.get('response')
        
        # Tokenize user response into sentences
        sentences = user_response.split('.')
        
        # Initialize counters
        total_sentences = len(sentences)
        stress_count = 0
        
        # List to store predictions for each sentence
        sentence_predictions = []
        
        # Iterate through each sentence
        for sentence in sentences:
            # Send sentence to Flask API for prediction
            prediction = send_to_flask_api(sentence)
            sentence_predictions.append(prediction)
            if prediction == 'Stress':
                stress_count += 1
        
        # Calculate stress level percentage
        stress_percentage = (stress_count / total_sentences) * 100
        
        # Return stress level percentage, stress count, and predictions to frontend
        response_data = {
            'stress_percentage': stress_percentage,
            'stress_count': stress_count,
            'sentence_predictions': sentence_predictions
        }
        return JsonResponse(response_data)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
def send_to_flask_api(sentence):
    # Send sentence to Flask API for prediction
    url = 'http://127.0.0.1:8001/predict'  # Replace with your Flask API endpoint
    data = {'response': sentence}
    response = HttpRequest().POST(url, json=data)
    prediction = response.json()['prediction']
    return prediction