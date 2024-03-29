from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4
from .models import User
from .models import Doctor
from .models import Chats
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
        chats       = data.get('chats')
        chats = data.get('chats')
        text = chats.get('text') if chats else None
        is_stress_checked = chats.get('is_stress_checked') if chats else False

        if (User.objects.filter(username = username).count() > 0 or User.objects.filter(email = email).count() > 0):
            return JsonResponse({'message': 'User already exists'}, status=400)
        
        user = User.create_user(email=email, name=name, dob=dob, gender=gender, text=text, is_stress_checked=is_stress_checked,
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
            # Password matches. Handle successful login
            token = str(uuid4())
            user['auth_token'] = token
            user.save()
            return JsonResponse({
                'message': 'Login successful',
                "token":token
                }, status=200)
        else:
            print('nooo')
            return JsonResponse({'message':'Login unsuccesssful'}, status=401)


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
def update_chat_data(request: HttpRequest):
    if request.method == 'POST':
        token = request.headers.get('Authorization')
        parts = token.split()
        auth_token = parts[1]
        data = json.loads(request.body)

        try:
            user = User.objects.get(auth_token=auth_token)
            text = data.get('text')
            is_stress_checked = data.get('is_stress_checked')
            new_chat = Chats(text=text, is_stress_checked=is_stress_checked)
            user.chats.append(new_chat)
            user.save() 
            return JsonResponse({"message":"Chat added successfully"}, status=200)
        except Exception as e:
            print(e)  
            return JsonResponse({"message":"The chat was not added to the system"}, status=405)
        

@csrf_exempt
def get_stress_data(request: HttpRequest):
    if request.method == 'GET':
        token = request.headers.get('Authorization')
        parts = token.split()
        auth_token = parts[1]
        user = User.objects(uuid=auth_token).first()
        stress_data = user.stress_level

        return JsonResponse({"stress_data": stress_data}, status=201)