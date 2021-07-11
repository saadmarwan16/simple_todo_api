from django.http import Http404
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task
from .serializers import TaskSerializer


class TaskList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.filter(owner=self.request.user)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=self.request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def is_user_authorized(self, owner):
        return self.request.user == owner

    def put(self, request, pk, format=None):
        task = self.get_object(pk)

        if not self.is_user_authorized(task.owner):
            return Response({'error': 'You are not authorized to update this task'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TaskSerializer(task, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)

        

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)

        if not self.is_user_authorized(task.owner):
            return Response({'error': 'You are not authorized to delete this task'}, status=status.HTTP_401_UNAUTHORIZED)

        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)