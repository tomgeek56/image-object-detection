from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from detection.detection_logic.detector import detectObjects
from detection.serializers import DetectionSerializer
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    )
    
class ImageDetectionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        image = request.data.get('image')
        print('image')
        obj = detectObjects(image)
        response_data = DetectionSerializer(obj, many=True).data
        for o in obj:
            print(type(o))
            print(o.x)
            
        return Response(data=response_data)
