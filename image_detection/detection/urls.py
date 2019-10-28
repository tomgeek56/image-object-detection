from django.contrib import admin
from django.urls import path
from detection.views import (ImageDetectionView)
app_name = 'image-detection'

urlpatterns = [
    path('detect-image', ImageDetectionView.as_view())
]