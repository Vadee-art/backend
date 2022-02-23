from rest_framework.decorators import api_view
from artworks.serializer import ArticleSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from artworks.models import Article, Artwork
from rest_framework import status


@api_view(['GET'])
def fetchTheArticle(request):
    article = Article.objects.all()
    serializer = ArticleSerializer(article, many=True)
    return Response(serializer.data)
