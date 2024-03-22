from mongoengine import Document, fields
from uuid import uuid4
import bcrypt

class User(Document):
    email           = fields.EmailField(required=True)
    name            = fields.StringField(required=True)
    date_of_birth   = fields.DateField()
    gender          = fields.StringField(blank=True)
    occupation      = fields.StringField(blank=True)
    username        = fields.StringField(unique=True, required=True)
    password        = fields.StringField(required=True)
    interests       = fields.ListField(fields.StringField(blank=True))
    chats           = fields.ListField(fields.StringField(blank=True))
    auth_token      = fields.StringField(unique=True, blank=True)

    meta={
        'db_alias' : 'users_data'
    }

    @classmethod
    def create_user(cls, email, name, dob, gender, occupation, username, password, interests):
        # Hashing password to store it securely
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        token = str(uuid4())
        user = cls(email=email, name=name, date_of_birth=dob, gender=gender, auth_token=token,
                    occupation=occupation, username=username, password=hashed_password, interests=interests)
        return user
    

class Doctor(Document):
    name            = fields.StringField(required=True)
    specialisation  = fields.StringField(required=True)
    description     = fields.StringField(required=True)
    experience      = fields.StringField(required=True)
    charge          = fields.DecimalField(required=True)
    profile_picture = fields.FileField()


    meta={
        'db_alias' : 'default'
    }

    @classmethod
    def create_doctor(cls, name, specialisation, description, experience, charge):
        doctor = cls(name=name, specialisation=specialisation, description=description, experience=experience,
                     charge=charge)
        return doctor


class Booking(Document):
    user = fields.ReferenceField(User, required=True)  # Reference to the User who booked
    doctor = fields.ReferenceField(Doctor, required=True)  # Reference to the booked Doctor
    date = fields.DateTimeField(required=True)
    time = fields.DateTimeField(required=True)