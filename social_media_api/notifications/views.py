from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer  # Assuming you have a serializer for Notification

    def get_queryset(self):
        # Fetch notifications for the authenticated user
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class NotificationReadView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    
    def patch(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.read = True  # Assuming you have a 'read' field in your Notification model
        notification.save()
        return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)
