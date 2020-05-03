from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission
from .models import Token

from .utils import recaptcha_validation

# Custom Unauthorized Error
class UnauthorizedError(APIException):
    status_code = 401
    default_detail = "Unauthorized."
    default_code = "Unauthorized."


# Custom Perimission Class
class HasPerimission(BasePermission):

    # this func search request token in .models.Token
    def has_permission(self, request, view):
        if  request.META['PATH_INFO'] == '/api/v1/links/' and \
            request.method == 'POST' and \
            recaptcha_validation(request):
                return True

        token = request.headers.get('Authorization')
        if not token:
            raise UnauthorizedError()
        try:
            request.user = Token.objects.get(token=token).user
            return True
        except Token.DoesNotExist:
            raise UnauthorizedError()