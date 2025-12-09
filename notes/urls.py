
# notes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnitViewSet, SubtopicViewSet, PDFViewSet, ImageUploadView

router = DefaultRouter()
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'subtopics', SubtopicViewSet, basename='subtopic')
router.register(r'pdfs', PDFViewSet, basename='pdf')

urlpatterns = [
    path('', include(router.urls)),
    path('upload-image/', ImageUploadView.as_view(), name='upload-image'),  # NEW
]

