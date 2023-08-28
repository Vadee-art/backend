from rest_framework.exceptions import APIException, status


class ArtworkSoldOut(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = "Artwork sold out"
    default_code = 'ArtworkSoldOut'