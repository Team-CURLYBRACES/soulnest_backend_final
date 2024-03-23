from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('register_doctor/', views.register_doctor),
    path('get_details/', views.get_doctor_details),
    path('response/', views.predict_stress_percentage),
]