from django.http import JsonResponse, HttpRequest, HttpResponse
from .models import User
from .models import Doctor
from django.views.decorators.csrf import csrf_exempt
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
            user.save(using='users')
            print('here')
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt        
def login_user(request: HttpRequest):
    print('here')
    data = json.loads(request.body)
    print(data)

    if (request.method == 'POST'):
        email = data.get('email')
        password = data.get('password')

        user = User.objects(email=email).first()
        print(user.name)
        if user and bcrypt.checkpw(password.encode(), user.password.encode()):
            # Password matches! Handle successful login
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'message':'Login unsuccesssful'})
     

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
        doctor.profile_picture.put(profile_picture, content_type = profile_picture.content_type)
        
        try:
            doctor.save()
            return JsonResponse({'message': 'Doctor registered successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def get_doctor_details(request : HttpRequest):
    doctor_profiles = []
    doctors = Doctor.objects().all()
    #photo = doctor.profile_picture.read()
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
