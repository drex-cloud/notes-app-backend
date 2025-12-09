from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Unit, Subtopic, PDF

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PDFSerializer(serializers.ModelSerializer):
    # This tells Django: "Accept a number (ID) for subtopic"
    subtopic = serializers.PrimaryKeyRelatedField(queryset=Subtopic.objects.all())
    
    class Meta:
        model = PDF
        # I removed the read_only part for 'file'. Now Django will accept the upload.
        fields = ['id', 'title', 'file', 'uploaded_at', 'subtopic']
        
    def to_representation(self, instance):
        """Optional: Ensures the frontend gets the full Cloudinary URL"""
        representation = super().to_representation(instance)
        if instance.file:
            representation['file'] = instance.file.url
        return representation

class SubtopicSerializer(serializers.ModelSerializer):
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    # Nested serializer so you can see PDFs inside the subtopic
    pdfs = PDFSerializer(many=True, read_only=True)

    class Meta:
        model = Subtopic
        fields = ['id', 'unit', 'title', 'notes', 'pdfs']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name']
    
    def create(self, validated_data):
        # Automatically attach the logged-in user
        user = self.context["request"].user
        return Unit.objects.create(user=user, **validated_data)