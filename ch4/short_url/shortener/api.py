from rest_framework import status
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from shortener.models import ShortURL
from shortener.serializers import ShortURLResponseSerializer, ShortURLCreateSerializer


class ShortURLAPIView(ListCreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLResponseSerializer

    def perform_create(self, serializer):
        while True:
            code = ShortURL.generate_code()
            if not ShortURL.objects.filter(code=code).exists():
                break

        serializer.save(code=code)

    def create(self, request, *args, **kwargs):
        serializer = ShortURLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            data=ShortURLResponseSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED
        )

class ShortURLDetailAPIView(DestroyAPIView):
    queryset = ShortURL.objects.all()
    lookup_field = "code"


class ShortURLViewSet(
    ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLResponseSerializer
    lookup_field = "code"

    def perform_create(self, serializer):
        while True:
            code = ShortURL.generate_code()
            if not ShortURL.objects.filter(code=code).exists():
                break

        serializer.save(code=code)

    def create(self, request, *args, **kwargs):
        serializer = ShortURLCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            data=ShortURLResponseSerializer(serializer.instance).data,
            status=status.HTTP_201_CREATED
        )
