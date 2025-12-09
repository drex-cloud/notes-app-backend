# notes/views.py

import os
import uuid

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.files.storage import default_storage 

from rest_framework import viewsets, status, permissions, parsers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
# JSONParser is CRITICAL for the rename button to work
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser 
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Unit, Subtopic, PDF
from .serializers import (
    UnitSerializer,
    SubtopicSerializer,
    PDFSerializer,
)

# ---------------------------
# Unit ViewSet
# ---------------------------
class UnitViewSet(viewsets.ModelViewSet):
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Unit.objects.filter(user=self.request.user)

    @action(detail=True, methods=["post"])
    def add_subtopic(self, request, pk=None):
        unit = self.get_object()
        title = request.data.get("title")
        if not title:
            return Response({"error": "Title required"}, status=status.HTTP_400_BAD_REQUEST)
        sub = Subtopic.objects.create(unit=unit, title=title)
        serializer = SubtopicSerializer(sub)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------
# Subtopic ViewSet
# ---------------------------
class SubtopicViewSet(viewsets.ModelViewSet):
    serializer_class = SubtopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subtopic.objects.filter(unit__user=self.request.user)

    def create(self, request, *args, **kwargs):
        unit_id = request.data.get("unit")
        title = request.data.get("title")
        notes = request.data.get("notes", "")

        if not unit_id:
            return Response({"error": "unit is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            unit = Unit.objects.get(id=unit_id, user=request.user)
        except Unit.DoesNotExist:
            return Response({"error": "Unit not found"}, status=status.HTTP_404_NOT_FOUND)

        subtopic = Subtopic.objects.create(unit=unit, title=title, notes=notes)
        serializer = SubtopicSerializer(subtopic)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------
# PDF ViewSet (The fix for Rename and Upload)
# ---------------------------
class PDFViewSet(viewsets.ModelViewSet):
    serializer_class = PDFSerializer
    permission_classes = [IsAuthenticated]
    
    # 1. MultiPart/FormParser = Allows File Uploads
    # 2. JSONParser = Allows Renaming (Patch requests with JSON)
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        return PDF.objects.filter(subtopic__unit__user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subtopic = serializer.validated_data['subtopic']
        if subtopic.unit.user != request.user:
            return Response({"error": "You do not own this subtopic"}, status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------------
# Auth: Register/Login
# ---------------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email", "")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create(
        username=username,
        email=email,
        password=make_password(password),
    )

    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "username": user.username,
    })


# ---------------------------
# Image Upload (Quill Editor)
# ---------------------------
class ImageUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        image = request.FILES.get("image")
        if not image:
            return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        if image.size > 5 * 1024 * 1024:
            return Response({"error": "Image too large (max 5MB)"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Uses default_storage (Cloudinary) to save
            file_path = default_storage.save(f"quill_uploads/{uuid.uuid4()}_{image.name}", image)
            file_url = default_storage.url(file_path)
            return Response({"url": file_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Upload error:", e)
            return Response({"error": "Failed to upload image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)