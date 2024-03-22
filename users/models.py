from mongoengine import Document, fields
import bcrypt

class User(Document):
    email           = fields.EmailField()
    name            = fields.StringField()
    date_of_birth   = fields.DateField()
    gender          = fields.StringField()
    occupation      = fields.StringField()
    username        = fields.StringField(unique=True, required=True)
    password        = fields.StringField(required=True)
    interests       = fields.ListField(fields.StringField())

    meta={
        'db_alias' : 'users'
    }

    @classmethod
    def create_user(cls, email, name, dob, gender, occupation, username, password, interests):
        # Hashing password to store it securely
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = cls(email=email, name=name, date_of_birth=dob, gender=gender,
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