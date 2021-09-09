from rest_framework import mixins, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from serv.models.photo import Photo
from serv.permissions.photo import HasPermissionsForPhoto
from serv.serializers.photos import PhotoSerializer


class PhotoView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    model = Photo
    serializer_class = PhotoSerializer
    permission_classes = (HasPermissionsForPhoto,)
    parser_classes = (MultiPartParser,)

    queryset = model.objects

    def create(self, request, *args, **kwargs):
        context = self.get_serializer_context()
        serializer = PhotoSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        photo = serializer.save()
        photo.min_size_file_save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.add_view()
        return super().retrieve(self, request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
