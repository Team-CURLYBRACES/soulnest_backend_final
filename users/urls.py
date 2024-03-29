from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('register_doctor/', views.register_doctor),
    path('get_details/', views.get_doctor_details),
    path('update_chat/', views.update_chat_data),
    path('get_stress_info/', views.get_stress_data),
]