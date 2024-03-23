from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from .models import User
from .models import Doctor
import json
import bcrypt
import base64


@csrf_exempt 
def register_user(request: HttpRequest):

    json_data = request.body.decode('utf-8')
    data = json.loads(json_data)

    if request.method == 'POST':
        email       = data.get('email')
        name        = data.get('name')
        dob         = data.get('date_of_birth')
        gender      = data.get('gender')
        occupation  = data.get('occupation')
        username    = data.get('username')
        password    = data.get('password')
        interests   = data.get('interests')
        
        if (User.objects.filter(username = username).count() > 0 or User.objects.filter(email = email).count() > 0):
            return JsonResponse({'message': 'User already exists'}, status=400)
        
        user = User.create_user(email=email, name=name, dob=dob, gender=gender,
                                 occupation=occupation, username=username, password=password, interests=interests)
        try:
            user.save(using='users_data')
            return JsonResponse({
                'message': 'User registered successfully',
                'id': user.name
                }, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt        
def login_user(request: HttpRequest):
    data = json.loads(request.body)

    if (request.method == 'POST'):
        email = data.get('email')
        password = data.get('password')

        user = User.objects(email=email).first()
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            # Password matches! Handle successful login
            token = str(uuid4())
            user['auth_token'] = token
            user.save()
            return JsonResponse({
                'message': 'Login successful',
                'id': str(user.id),
                "token":token
                }, status=200)
        else:
            return JsonResponse({'message':'Login unsuccesssful'})


@csrf_exempt
def get_user_details(request: HttpRequest):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        user = User.objects(email=email).first()
        return JsonResponse({
            "name": user.name
        })


@csrf_exempt
def register_doctor(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name')
        specialisation = request.POST.get('specialisation')
        description = request.POST.get('description')
        experience = request.POST.get('experience')
        charge = request.POST.get('charge')
        profile_picture = request.FILES.get('picture')

        doctor = Doctor.create_doctor(name=name, specialisation=specialisation, description=description, experience=experience,
                     charge=charge)
        if profile_picture:
            doctor.profile_picture.put(profile_picture, content_type = profile_picture.content_type)
        try:
            doctor.save()
            return JsonResponse({'message': 'Doctor registered successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def get_doctor_details(request : HttpRequest):
    if request.method == 'GET':
        doctor_profiles = []
        doctors = Doctor.objects().all()

        for doctor in doctors:
            profile_image_data = None
            if doctor.profile_picture:
                profile_image_data = base64.b64encode(doctor.profile_picture.read()).decode('utf-8')

            doctor_profiles.append({
            'name': doctor.name,
            'specialisation': doctor.specialisation,
            'description': doctor.description,
            'experience': doctor.experience,
            'charge': doctor.charge,
            'image': profile_image_data
        })
    return JsonResponse(doctor_profiles, safe=False)

@csrf_exempt
def predict_stress_percentage(request: HttpRequest):
    if request.method == 'POST':
        # Receive user response from frontend
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

