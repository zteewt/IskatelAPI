from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import PointSerializer, MessageSerializer
from .models import Point as Point_model
from .models import Messages
from django.contrib.gis.geos import Point  
from django.contrib.gis.db.models.functions import Distance
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


class PointViewSet(viewsets.ModelViewSet):
    queryset = Point_model.objects.all()
    serializer_class = PointSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    @action(detail=False, methods=["get", "post"])
    def messages(self, request, pk=None):
        """
        POST NEW MESSAGE TO POINT
        URL: /api/points/messages   
        """
        if request.method == 'POST':
            point_id = request.data.get('point')
            data = {'message': request.data['message'], 'point': point_id}
            serializer = MessageSerializer(data=data, context={"request": request})
            if serializer.is_valid(raise_exception=True):
                msg = serializer.save()
                return Response(serializer.data)

        """
        GET ALL MESSAGES 
        URL: /api/points/messages/
        """
        messages = Messages.objects.select_related('point')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=["get"], url_path='messages') 
    def point_messages(self, request, pk=None):
        """
        GET MESSAGES BY SPECIFIC POINT
        URL: /api/points/{point_id}/messages/
        """
        point = self.get_object()
        messages = Messages.objects.filter(point=point, user=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)



    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        SEARCH POINTS IN SPECIFIC AREA
        Query params: latitude, longitude and radius
        URL: /api/points/search/
        """
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
            radius_meters = float(request.query_params.get('radius')) * 1000

            center_point = Point(longitude, latitude, srid=4326)
            
            points = Point_model.objects.annotate(
                distance=Distance('location', center_point)
            ).filter(
                distance__lt=radius_meters
            ).order_by('distance')
            
            serializer = self.get_serializer(points, many=True)
            return Response(serializer.data)
        
        except (TypeError, ValueError):
            return Response({"error": "invalid params"}, status=400)
    


    @action(detail=False, methods=["get"], url_path="messages/search")
    def messages_search(self, request):
        """
        SEARCH MESSAGES IN SPECIFIC AREA 
        Query params: latitude, longitude and radius
        URL: /api/points/messages/search/
        """
        try:
            latitude = float(request.query_params.get('latitude'))   
            longitude = float(request.query_params.get('longitude'))
            radius_meters = float(request.query_params.get('radius')) * 1000

            center_point = Point(longitude, latitude, srid=4326)
            
            messages = Messages.objects.annotate(
                distance=Distance('point__location', center_point)
            ).filter(
                distance__lt=radius_meters
            ).order_by('distance')
            
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        
        except (TypeError, ValueError):
            return Response({"error": "invalid params"}, status=400)