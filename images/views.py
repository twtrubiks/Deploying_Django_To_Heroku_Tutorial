from django.shortcuts import render
from rest_framework import viewsets

from images.models import Image
from images.serializers import ImageSerializer
from ptt_beauty_images import settings


# single-databases
def index_old(request):
    return render(request, 'index.html', {
        'images': Image.objects.values('id', 'Url').order_by('-CreateDate')
    })


# multiple-databases
def index(request):
    images_seq = []
    for db_name in settings.DATABASES:
        query = Image.objects.using(db_name).all()
        for data in query:
            dict_image = {
                'id': data.id,
                'Url': data.Url,
                'CreateDate': data.CreateDate
            }
            images_seq.append(dict_image)
    images_seq = sorted(images_seq, key=lambda x: x['CreateDate'], reverse=True)
    return render(request, 'index.html', {
        'images': images_seq
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
