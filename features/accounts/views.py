from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
def register(request, format=None):
    data = request.data

    # Ensure password matches confirmation
    password = data['password']
    confirmation = data['confirmation']
    if password != confirmation:
        return Response({'error': 'Passwords must match.'}, status=status.HTTP_400_BAD_REQUEST)

    # Attempt to create new user
    try:
        user = User.objects.create_user(first_name=data['first_name'], last_name=data['last_name'], username=data['username'], password=password)
        user.save()
        return Response({'success': 'New user created successfully'}, status=status.HTTP_201_CREATED)
    except IntegrityError as e:
        print(e)
        return Response({'error': 'Email address already taken.'}, status=status.HTTP_400_BAD_REQUEST)