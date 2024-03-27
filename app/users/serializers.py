# from rest_framework import serializers
# from .models import User
# from .models import Doctor

# class UserSerializer(serializers.DocumentSerializers):
#     class Meta:
#         model   = User
#         fields  = '__all__'

# class CreateUserSerializer(serializers.ModelSerializer):
#     interests = serializers.ListField(child=serializers.CharField())  # Serializer for the list of strings
    
#     class Meta:
#         model = User
#         fields = '__all__'


# class DoctorSerializer(serializers.DocumentSerializers):
#     class Meta:
#         model   = Doctor
#         fields  = ['name', 'specialisation', 'description', 'experience', 'charge']