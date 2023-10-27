from artworks.models import Article
from artworks.serializer import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def fetchTheArticle(request):
    article = Article.objects.all()
    serializer = ArticleSerializer(article, many=True)
    return Response(serializer.data)
