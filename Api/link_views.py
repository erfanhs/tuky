from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import linkSerializer
from .Authentication import HasPerimission

from .models import Link, Report, User

from main.utils import save_click_details
from .utils import check_input_data, ClickAnalyse, password_hashing

import re



class link_collection(APIView):

    permission_classes = (HasPerimission,)

    # list of user links
    def get(self, request, format=None):

        user = request.user

        search = request.GET.get('search')
        limit = request.GET.get('limit')
        skip = request.GET.get('skip')
        all_ = request.GET.get('all')

        if all_ == 'false' or all_ == '0': all_ = False
        if all_ == None: all_ = True
        if limit == None: limit = '0'
        if skip == None: skip = '0'
        
        if not limit.isdigit():
            return Response({'error': 'limit field must be digits !'})
        if not skip.isdigit():
            return Response({'error': 'skip field must be digits !'})

        if search:
            links = Link.objects.filter(user=user, url_id__contains=search) | Link.objects.filter(user=user, long_url__contains=search)
        else:
            links = Link.objects.filter(user=user)

        serializer = linkSerializer(links.order_by('-dateTime'), many=True)
    
        if all_:
            return Response(serializer.data)
        return Response(serializer.data[ int(skip) : int(skip) + int(limit) ])



    # create new link
    def post(self, request, format=None):

        user = None
        if type(request.user) == User:
            user = request.user

        if 'long_url' not in request.data:
            return Response({'error': 'فیلد لینک الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
 
        data = check_input_data(request.data)
        if 'error' in data: return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
        if hasattr(data, '_mutable'): data._mutable = True
        if user: data['user'] = user.pk

        serializer = linkSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # delete all user links
    def delete(self, request, format=None):

        user = request.user

        links = Link.objects.filter(user=user)
        if links:
            links.delete()
            return Response({'Response': 'تمامی لینک ها با موفقیت حذف شدند !'})
        return Response({'Response': 'هیچ لینکی برای حذف موجود نمی باشد !'})



class link_element(APIView):

    permission_classes = (HasPerimission,)

    # get link details
    def get(self, request, url_id):

        user = request.user

        try:
            link = Link.objects.get(url_id=url_id)
            if not link.user == user:
                return Response({'url_id': 'این لینک متعلق به شما نیست !'}, status=status.HTTP_403_FORBIDDEN)
            serializer = linkSerializer(link)
            return Response(serializer.data)
        except Link.DoesNotExist:
            return Response({'error': 'این لینک وجود ندارد !'}, status=status.HTTP_404_NOT_FOUND)


    # delete link
    def delete(self, request, url_id):

        user = request.user
        
        try:
            link = Link.objects.get(url_id=url_id)
            if not link.user == user:
                return Response({'error': 'این لینک متعلق به شما نیست !'}, status=status.HTTP_403_FORBIDDEN)
            link.delete()
            return Response({'status': 'لینک با موفقیت حذف شد.'})
        except Link.DoesNotExist:
            return Response({'error': 'این لینک وجود ندارد !'}, status=status.HTTP_404_NOT_FOUND)


    # update link
    def put(self, request, url_id):

        user = request.user

        data = request.data
        if hasattr(data, '_mutable'):
            data._mutable = True

        for key in data:
            if key not in ['url_id', 'long_url', 'expiration_date']:
                return Response({'error': 'فیلد ناشناخته !'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            link = Link.objects.get(url_id=url_id)
            if not link.user == user:
                return Response({'error': 'این لینک متعلق به شما نیست !'}, status=status.HTTP_403_FORBIDDEN)
            

            if 'long_url' not in data: data['long_url'] = link.long_url

            if 'url_id' in data and url_id == data['url_id']:
                del data['url_id']

            data = check_input_data(data)
            if 'error' in data: return Response(data, status=status.HTTP_400_BAD_REQUEST)

            serializer = linkSerializer(link, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Link.DoesNotExist:
            return Response({'error': 'این لینک وجود ندارد !'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
@permission_classes([HasPerimission])
def linkStats(request, url_id):

    user = request.user

    try:
        link = Link.objects.get(url_id=url_id)
        if not link.user == user:
            return Response({'error': 'این لینک متعلق به شما نیست !'}, status=status.HTTP_403_FORBIDDEN) 

        Analyser = ClickAnalyse(link)
        lastDayAnalyse = Analyser.day()
        lastWeekAnalyse = Analyser.week()
        lastMonthAnalyse = Analyser.month()
        allTimeAnalyse = Analyser.alltime()
        del Analyser

        return Response({
            'lastDay': lastDayAnalyse,
            'lastWeek': lastWeekAnalyse,
            'lastMonth': lastMonthAnalyse,
            'allTime': allTimeAnalyse
        })

    except Link.DoesNotExist:
        return Response({'error': 'این لینک وجود ندارد !'}, status=status.HTTP_404_NOT_FOUND)




@api_view(['POST'])
def checkLinkPassword(request, url_id):
    password = request.data.get('password')
    if not password:
        return Response({'error': 'فیلد پسورد الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        link = Link.objects.get(url_id=url_id)
        if not link.password:
            save_click_details(request, link)
            return Response({'message':'این لینک پسورد ندارد !', 'longUrl': link.long_url})
        if link.password != password_hashing(password):
            return Response({'error': 'رمز عبور اشتباه است !'}, status=status.HTTP_400_BAD_REQUEST)
        save_click_details(request, link)
        return Response({'longUrl': link.long_url})
    except Link.DoesNotExist:
        return Response({'error': 'این لینک وجود ندارد !'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def ReportLink(request):
    short_url = request.GET.get('short_url')
    
    if not short_url: return Response({'error': 'فیلد لینک الزامی است !'}, status=status.HTTP_400_BAD_REQUEST)
    
    result = re.findall('tuky.ir\/([a-zA-Z0-9]*)$', short_url)
    if result:
        try:
            link = Link.objects.get(url_id=result[0])
            Report.objects.create(short_url=link)
            return Response({'response': 'ممنون از گزارش شما ، ما به زودی اقدام خواهیم کرد.'})
        except Link.DoesNotExist:
            return Response({'error': 'لینک مورد نظر یافت نشد !'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'لینک وارد شده اشتباه است !'}, status=status.HTTP_400_BAD_REQUEST)
