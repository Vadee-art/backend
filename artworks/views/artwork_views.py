from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from artworks.serializer import ArtworkSerializer
from django.contrib.auth.models import User
from artworks.models import Artwork, Artist
from rest_framework import status
from artworks.serializer import UserSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# from ..forms import ClassificationForm

# # form views
# def formView(request):
#     context = {}
#     context['form'] = ClassificationForm()
#     return Response(context)


@api_view(['GET'])
def fetchArtWorks(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    # we could use any value instead of title
    artworks = Artwork.objects.filter(
        title__icontains=query).order_by('createdAt')

    # pagination
    page = request.query_params.get('page')
    p = Paginator(artworks, 8)

    try:
        artworks = p.page(page)
    except PageNotAnInteger:  # first render we have no page
        artworks = p.page(1)
    except EmptyPage:  # page does not exist return the last page
        artworks = p.page(p.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = ArtworkSerializer(artworks, many=True)
    return Response({'artworks': serializer.data, 'page': page, 'pages': p.num_pages})


@api_view(['GET'])
def fetchTheArtWork(request, pk):
    artwork = Artwork.objects.get(_id=pk)
    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createTheArtWork(request):
    user = request.user
    artist = Artist.objects.first()
    if user and artist:
        artwork = Artwork.objects.create(
            accountOwner=user,
            artist=artist,
            title='Default Title',
            subtitle='Default Subitle',
            aboutWork='سرزمین ایران، میزبان تمدن‌های کهنی چون ایلام، جیرفت و زاینده‌رود بوده‌است. نخستین‌بار در سدهٔ هفتم پیش از میلاد، در دوران پادشاهی ماد بود که بخش‌های قابل توجهی از فلات ایران یکپارچه شد. در سدهٔ ششم پ. م، شاهنشاهی هخامنشی توسط کوروش بزرگ بنیان نهاده شد تا ایران یکی از بزرگ‌ترین امپراتوری‌های تاریخ را تشکیل دهد. در سدهٔ چهارم پ. م، اسکندر مقدونی این امپراتوری را پایان داد و ایران به بخشی از ممالک هلنیستی تبدیل شد. پدیداری شاهنشاهی اشکانی در سدهٔ سوم پ. م، بار دیگر این کشور را تحت فرمان یک شاهنشاهی ایرانی قرار داد. در سدهٔ سوم م، شاهنشاهی ساسانی، یک امپراتوری گستردهٔ دیگر، در ایران به قدرت رسید و برای چهار سده بر سرزمینی پهناور حکومت کرد و مزدیسنا به دین غالب آن، تبدیل شد. ایران در این دوران نیز درگیر جنگ‌های مستمر و فرساینده با روم بود که به تضعیف کشور انجامید. در میانه‌های سدهٔ هفتم م، مسلمانان، امپراتوری ساسانی را سرنگون کردند و اسلام را به جای دین‌های ایرانی، رواج دادند. از دوران خلافت اسلامی تا سدهٔ سیزدهم، فعالیت‌های ادبی، علمی و هنری ایرانی نه تنها پایان نیافت، بلکه بار دیگر به شکوفایی رسید و ایرانیان مشارکتی اثرگذار در شکل‌گیری دوران طلایی اسلام داشتند. از سدهٔ نهم م، میان‌دورهٔ ایرانی آغاز شد و نخستین حکومت‌های ایرانی‌تبار پس از اسلام، پدیدار شدند. در سدهٔ دهم م، اقوام ترک به این کشور آمدند و حکومت‌هایی را تشکیل دادند که بر بخش بزرگی از ایران، حکومت می‌کردند. از سدهٔ ۱۳ م، حملهٔ مغول به ایران روی داد که به تشکیل ایلخانان انجامید و پس از آن، امپراتوری تیموری پدیدار ش',
            provenance='ایران کنونی، یک جمهوری اسلامی با بخش قانون‌گذار است و این نظام ترکیبی، تحت نظر رهبر آن، سید علی خامنه‌ای قرار دارد. ایران از اعضای مؤسس سازمان ملل متحد، سازمان همکاری اقتصادی، سازمان همکاری اسلامی و اوپک است و از قدرت‌های منطقه‌ای شمرده می‌شود. ایران، زیرساخت قابل توجهی در بخش‌های خدماتی، صنعتی و کشاورزی دارد که اقتصاد این کشور را توانمند می‌سازند اما این اقتصاد هنوز بر فروش نفت و گاز متکی است و از فساد مالی رنج می‌برد. منابع طبیعی ایران، قابل توجه هستند و در میان اعضای اوپک، ایران سومین دارندهٔ ذخایر بزرگ اثبات شدهٔ نفت است. میراث فرهنگی این کشور، غنی است و فهرست میراث جهانی یونسکو در ایران از ۲۴ مورد تشکیل می‌شود. ',
            width=0,
            height=0,
            depth=0,
            price=0,
        )
        serializer = ArtworkSerializer(artwork, many=False)
        return Response(serializer.data)
    else:
        return Response('هیچ هنرمندی وچود ندارد')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateTheArtwork(request, pk):
    data = request.data
    artwork = Artwork.objects.get(_id=pk)
    artist = Artist.objects.get(_id=data['artist'])
    accountOwner = User.objects.get(id=data['accountOwner'])
    artwork.accountOwner = accountOwner
    artwork.artist = artist
    artwork.title = data['title']
    artwork.subtitle = data['subtitle']
    artwork.year = data['year']
    artwork.category = data['category']
    artwork.medium = data['medium']
    artwork.condition = data['condition']
    artwork.classifications = data['classifications']
    artwork.width = data['width']
    artwork.height = data['height']
    artwork.depth = data['depth']
    artwork.unit = data['unit']
    artwork.isAnEdition = data['isAnEdition']
    artwork.editionNum = data['editionNum']
    artwork.editionSize = data['editionSize']
    artwork.isSigned = data['isSigned']
    artwork.isAuthenticated = data['isAuthenticated']
    artwork.frame = data['frame']
    artwork.isPrice = data['isPrice']
    artwork.price = data['price']
    artwork.aboutWork = data['aboutWork']
    artwork.provenance = data['provenance']
    artwork.artLocation = data['artLocation']
    artwork.quantity = data['quantity']

    artwork.save()
    serializer = ArtworkSerializer(artwork, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteTheArtwork(request):
    data = request.data
    selectedArtworks = data['selectedArtworks']
    for _id in selectedArtworks:
        artworkDeleting = Artwork.objects.get(_id=_id)
        artworkDeleting.delete()
    return Response('artworks were deleted')


@api_view(['POST'])
# @permission_classes([IsAdminUser])
def uploadImage(request):
    data = request.data
    artwork_id = data['artworkId']
    artwork = Artwork.objects.get(_id=artwork_id)

    artwork.image = request.FILES.get('image')
    artwork.save()
    return Response('عکس شما در دیتابیس ذخیره شد')
