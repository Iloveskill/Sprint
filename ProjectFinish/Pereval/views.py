import django_filters
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import *
from .models import *


class UsersViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['fam', 'name', 'otc', 'email']


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalsViewset(viewsets.ModelViewSet):
    queryset = Perevals.objects.all()
    serializer_class = PerevalsSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['beauty_title', 'title', 'add_time', 'user__email']

    def create(self, request,  *args, **kwargs):
        if self.action == 'create':
            serializer = PerevalsSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'message': 'Успех!',
                        'id': serializer.instance.pk,
                    }
                )

            if status.HTTP_400_BAD_REQUEST:
                return Response(
                    {
                        'status': status.HTTP_400_BAD_REQUEST,
                        'message': 'Некорректный запрос',
                        'id': None,
                    }
                )

            if status.HTTP_500_INTERNAL_SERVER_ERROR:
                return Response(
                    {
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': 'Ошибка при выполнении операции',
                        'id': None,
                    }
                )
        return super().create(request, *args, **kwargs)


    def partial_update(self, request, *args, **kwargs):
        if self.action == 'partial_update':
            instance = self.get_object()
            serializer = PerevalsUpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                serializer.save()

                validated_data['state'] = serializer.instance.state
                validated_data['message'] = serializer.instance.message

                return Response(validated_data)


        return super().partial_update(request, *args, **kwargs)


    def get_serializer_class(self):
        if self.action == 'partial_update':
            return PerevalsUpdateSerializer
        return super().get_serializer_class()
