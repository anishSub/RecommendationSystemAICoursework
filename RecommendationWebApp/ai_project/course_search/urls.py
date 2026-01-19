# course_search/urls.py
from django.urls import path
from . views import home, course_detail

urlpatterns = [
    path('', home, name='home'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
]