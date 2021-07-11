from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('<int:pk>/', views.UserDetail.as_view()),
    path('register/', views.register),
]

urlpatterns = format_suffix_patterns(urlpatterns)