from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from streamlit import status

from microaAdmin.api.serializers import *

from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterAPICreate(generics.CreateAPIView):
    permission_classes = [AllowAny]
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSelfDetail(generics.RetrieveAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    serializer_class = UserSerializerGET

    def get_object(self):
        return self.request.user

class PageAPIList(generics.ListAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

class SubpageAPIList(generics.ListAPIView):
    queryset = Subpage.objects.all()
    serializer_class = SubpageSerializer