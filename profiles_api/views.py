from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from elasticsearch_chat_app import *
from profiles_api import serializers, models, permissions


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class MessageSendApiView(APIView):
    """Send Message API"""
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username_src = request.user.username
            username_dest = serializer.validated_data.get('username')
            message = serializer.validated_data.get('message')
            send_message(es=es, username_src=username_src, username_dest=username_dest, message=message)
            return Response({'username_src': username_src, 'username_dest': username_dest, 'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewApiView(APIView):
    """Get all messages for logged in user"""
    serializer_class = serializers.MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        username = request.user.username
        return Response(get_messages(es=es, username=username))
