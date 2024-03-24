from mongoengine import Document, EmbeddedDocument, fields
from uuid import uuid4
import bcrypt



class Chats(EmbeddedDocument):
    text                = fields.StringField(blank=True)
    is_stress_checked   = fields.BooleanField(default=False)

class User(Document):
    email           = fields.EmailField(required=True)
    name            = fields.StringField(required=True)
    date_of_birth   = fields.DateField()
    gender          = fields.StringField(blank=True)
    occupation      = fields.StringField(blank=True)
    username        = fields.StringField(unique=True, required=True)
    password        = fields.StringField(required=True)
    interests       = fields.ListField(fields.StringField(blank=True))
    chats           = fields.ListField(fields.EmbeddedDocumentField(Chats))
    auth_token      = fields.StringField(unique=True, blank=True)
    stress_level    = fields.ListField(fields.DecimalField(blank=True))

    meta={
        'db_alias' : 'users_data'
    }

    @classmethod
    def create_user(cls, email, name, dob, gender, occupation, username, password, interests, text=None, is_stress_checked=False):
        
        chats = [Chats(text=text, is_stress_checked=is_stress_checked)] if text else []
        # Hashing password to store it securely
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        token = str(uuid4())
        user = cls(email=email, name=name, date_of_birth=dob, gender=gender, auth_token=token, chats=chats,
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