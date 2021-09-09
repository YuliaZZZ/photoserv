from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from serv.models.photo import Photo
from serv.serializers.toplist import TopListSerializer


class TopListView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    model = Photo
    serializer_class = TopListSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        return Photo.objects.all()[:1]
