from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from artworks.models import Article, Artwork
from artworks.serializer import ArticleSerializer


@api_view(['GET'])
def fetchTheArticle(request):
    article = Article.objects.all()
    serializer = ArticleSerializer(article, many=True)
    return Response(serializer.data)
