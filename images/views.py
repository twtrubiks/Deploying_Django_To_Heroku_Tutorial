from django.shortcuts import render
from rest_framework import viewsets, status
from images.models import Images
from images.serializers import ImageSerializer

# from ptt_beauty_images import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models.aggregates import Count
from random import randint


# # single-databases
# def index_old(request):
#     return render(request, 'index.html', {
#         'images': Image.objects.values('id', 'Url').order_by('-CreateDate')
#     })


# # multiple-databases
# def index(request):
#     images_seq = []
#     for db_name in settings.DATABASES:
#         query = Image.objects.using(db_name).all()
#         for data in query:
#             dict_image = {
#                 'id': data.id,
#                 'Url': data.Url,
#                 'CreateDate': data.CreateDate
#             }
#             images_seq.append(dict_image)
#     images_seq = sorted(images_seq, key=lambda x: x['CreateDate'], reverse=True)
#     return render(request, 'index.html', {
#         'images': images_seq
#     })


# Create your views here.
class ImageViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Images.objects.all()
    serializer_class = ImageSerializer

    # [ GET ] /api/image/random/
    @action(detail=False, methods=["get"], url_path="random")
    def get_random_image(self, request):
        count = Images.objects.aggregate(count=Count("id"))["count"]
        random_index = randint(0, count - 1)
        obj = Images.objects.all()[random_index]
        result = ImageSerializer(obj)
        return Response(result.data, status=status.HTTP_200_OK)
