from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'admin/',
        'api/artworks/',
        'api/artworks/<id>',
        'api/artworks/<id>/favorite',
        'api/artworks/delete/<id>',
        'api/artworks/<update>/<id>',
    ]
    return Response(routes)
