from django.shortcuts import render
from rest_framework import viewsets

from images.models import Image
from images.serializers import ImageSerializer


def index(request):
    return render(request, 'index.html', {
        'images': Image.objects.values('id', 'Url').order_by('-CreateDate')
    })


# Create your views here.
class ImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
