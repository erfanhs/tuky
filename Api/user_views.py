from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .Authentication import HasPerimission

from .models import User, Token

from .utils import recaptcha_validation, send_verify_mail, password_hashing
from django.utils import timezone


@api_view(['POST'])
def UserSignup(request):

    email = request.data.get('email')
    password = request.data.get('password')

    if not recaptcha_validation(request):
        return Response({'error': 'توکن کپچا اشتباه است !'}, status=status.HTTP_403_FORBIDDEN)

    if not email:
        return Response({'error': 'فیلد ایمیل الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return Response({'error': 'فیلد پسورد الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        User.objects.get(email=email, verified=True)
        return Response({'error': 'از این ایمیل در یک اکانت دیگر استفاده شده است.'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        User(
            email=email,
            password=password_hashing(password),
            email_verify=send_verify_mail(email)
        ).save()
        return Response({'response': 'لینک ورود به ایمیل شما ارسال شد.'})




@api_view(['POST'])
def UserLogin(request):
    
    email = request.data.get('email')
    password = request.data.get('password')

    if not recaptcha_validation(request):
        return Response({'error': 'توکن کپچا اشتباه است !'}, status=status.HTTP_403_FORBIDDEN)

    if not email:
        return Response({'error': 'فیلد ایمیل الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
    if not password:
        return Response({'error': 'فیلد پسورد الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        if user.password == password_hashing(password):
            if user.verified:
                user.last_login_at = timezone.now()
                user.save()
                user_token = Token.objects.get(user=user).token
                return Response({'token': user_token, 'email': user.email})
            return Response({'error': 'ایمیل شما تایید نشده است !'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'error': 'رمز عبور اشتباه است !'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'ایمیل وارد شده اشتباه است !'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([HasPerimission])
def GetUser(request):
    user = request.user
    return Response({
        'email': user.email,
        'api_token': request.headers.get('Authorization')
    })



@api_view(['POST'])
@permission_classes([HasPerimission])
def ChangePassword(request):
    user = request.user
    old_password = request.data.get('opassword')
    new_password = request.data.get('npassword')
    if not old_password: 
        return Response({'error': 'پسورد فعلی الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
    if not new_password:
        return Response({'error': 'پسورد جدید الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
    if user.password != password_hashing(old_password):
        return Response({'error': 'پسورد وارد شده اشتباه است !'}, status=status.HTTP_400_BAD_REQUEST)
    user.password = password_hashing(new_password)
    user.save()
    return Response({'response': 'رمز عبور شما با موفقیت تغییر یافت.'})


@api_view(['POST'])
@permission_classes([HasPerimission])
def DeleteAccount(request):
    user = request.user
    password = request.data.get('password')
    if not password:
        return Response({'error': 'فیلد پسورد الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
    if user.password != password_hashing(password):
        return Response({'error': 'پسورد وارد شده اشتباه است !'}, status=status.HTTP_400_BAD_REQUEST)
    user.delete()
    return Response({'response': 'اکانت شما با موفقیت حذف شد.'})