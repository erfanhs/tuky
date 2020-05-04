from django.conf import settings
from django.core.mail import send_mail

from django.utils.crypto import get_random_string
from hashlib import md5, sha1

import re
import requests

import datetime
from dateutil.relativedelta import relativedelta
import pytz

from . import models


tz = pytz.timezone('Asia/Tehran')

class ClickAnalyse:

    def __init__(self, link):
        self.clicks = models.Click.objects.filter(short_url=link)
        self.now = datetime.datetime.now(tz)

    def os(self, clicks=None):
        if clicks == None: clicks = self.clicks
        
        OSs = [click.os for click in clicks]
        OSsClean = []
        [OSsClean.append(os) for os in OSs if os not in OSsClean]
        OSsCountJson = {}
        [OSsCountJson.update({os: OSs.count(os)}) for os in OSsClean]
        return OSsCountJson

    def browser(self, clicks=None):
        if clicks == None: clicks = self.clicks

        browsers = [click.browser for click in clicks]
        browsersClean = []
        [browsersClean.append(browser) for browser in browsers if browser not in browsersClean]
        browsersCountJson = {}
        [browsersCountJson.update({browser: browsers.count(browser)}) for browser in browsersClean]
        return browsersCountJson

    def device(self, clicks=None):
        if clicks == None: clicks = self.clicks

        devices = [click.device for click in clicks]
        devicesClean = []
        [devicesClean.append(device) for device in devices if device not in devicesClean]
        devicesCountJson = {}
        [devicesCountJson.update({device: devices.count(device)}) for device in devicesClean]
        return devicesCountJson

    def country(self, clicks=None):
        if clicks == None: clicks = self.clicks

        countries = [click.country for click in clicks]
        countriesClean = []
        [countriesClean.append(country) for country in countries if country not in countriesClean]
        countriesCountJson = {}
        [countriesCountJson.update({country: countries.count(country)}) for country in countriesClean]
        return countriesCountJson



    def roundClicks(self, clicks):
        for click in clicks:
            date = click.dateTime.astimezone(tz)
            if date.minute >= 30: date = date + datetime.timedelta(minutes=60 - date.minute)
            else: date = date - datetime.timedelta(minutes=date.minute)
            click.dateTime = date
        return clicks


    def day(self):
        def filterByHourDay(hour, day):
            return [click for click in clicks if click.dateTime.hour == hour and click.dateTime.day == day]
        now = self.now
        clicks = self.clicks.filter(dateTime__range=[now - relativedelta(days=1), now + datetime.timedelta(hours=1)])
        clicks = self.roundClicks(clicks)
        TimeLine_Day_List = [ len(filterByHourDay((now - datetime.timedelta(hours=i)).hour, (now - datetime.timedelta(hours=i)).day)) for i in range(0,24)]
        TimeLine_Day_List[0] += len(filterByHourDay((now + datetime.timedelta(hours=1)).hour, now.day))
        TimeLine_Day_List.reverse()
        return {
            'totalClicks': len(clicks),
            'browser': self.browser(clicks),
            'os': self.os(clicks),
            'country': self.country(clicks),
            'device': self.device(clicks),
            'timeLine': TimeLine_Day_List,
            'time_interval': 'lastDay'
        }      

    def week(self):
        now = self.now
        clicks = self.clicks.filter(dateTime__range = [now - datetime.timedelta(days=6), now + datetime.timedelta(days=1)])
        TimeLine_Week_List = [ len(clicks.filter(dateTime__day = (now - datetime.timedelta(days=i)).day)) for i in range(0, 7)]
        TimeLine_Week_List.reverse()
        return {
            'totalClicks': len(clicks),
            'browser': self.browser(clicks),
            'os': self.os(clicks),
            'country': self.country(clicks),
            'device': self.device(clicks),
            'timeLine': TimeLine_Week_List,
            'time_interval': 'lastWeek'
        }

    def month(self):
        now = self.now.date()
        clicks = self.clicks.filter(dateTime__range = [now - relativedelta(months=1), now + datetime.timedelta(days=1)])
        TimeLine_Month_List = [ len(clicks.filter(dateTime__date = (now - datetime.timedelta(days=i)))) for i in range(0, 30)]
        TimeLine_Month_List.reverse()
        return {
            'totalClicks': len(clicks),
            'browser': self.browser(clicks),
            'os': self.os(clicks),
            'country': self.country(clicks),
            'device': self.device(clicks),
            'timeLine': TimeLine_Month_List,
            'time_interval': 'lastMonth'
        }
        

    def alltime(self):
        now = self.now.date()
        clicks = self.clicks.filter(dateTime__range = [now - relativedelta(months=18), now + datetime.timedelta(days=1)])
        TimeLine_AllTime_List = [ len(clicks.filter(dateTime__month = (now - relativedelta(months=i)).month, dateTime__year = (now - relativedelta(months=i)).year )) for i in range(0, 18)]
        TimeLine_AllTime_List.reverse()
        return {
            'totalClicks': len(clicks),
            'browser': self.browser(clicks),
            'os': self.os(clicks),
            'country': self.country(clicks),
            'device': self.device(clicks),
            'timeLine': TimeLine_AllTime_List,
            'time_interval': 'allTime'
        }



def send_verify_mail(target):
	verify_id = get_random_string(length=32)
	send_mail(
		'email verify link',
		('thanks for sign up.\nverify link: http://%s/verify/' % settings.HOST_NAME) + verify_id,
		'erfanharirsaz071@gmail.com',
		[target],
		fail_silently=False
	)
	return verify_id


def password_hashing(passw):
	return sha1(md5(passw.encode('utf8')).hexdigest().encode('utf8')).hexdigest()


url_validator_regex = re.compile(re.compile(
    u"^"
    u"(?:(?:https?|ftp)://)"
    u"(?:\S+(?::\S*)?@)?"
    u"(?:"
    u"(?P<private_ip>"
    u"(?:(?:10|127)" + u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))" + u"{2}" + u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))" + u")|"
    u"(?:(?:169\.254|192\.168)" + u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))" + u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))" + u")|"
    u"(?:172\.(?:1[6-9]|2\d|3[0-1])" + u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))" + u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))" + u"))"
    u"|"
    u"(?P<public_ip>"
    u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    u"" + u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5]))" + u"{2}"
    u"" + u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))" + u")"
    u"|"
    u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    u")"
    u"(?::\d{2,5})?"
    u"(?:/\S*)?"
    u"(?:\?\S*)?"
    u"$",
    re.UNICODE | re.IGNORECASE
))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def recaptcha_validation(request):
    captcha_rs = request.data.get('recaptchaToken')
    if not captcha_rs: return False
    url = "https://www.google.com/recaptcha/api/siteverify"
    params = {
        'secret': settings.CAPTCHA_SECRET_KEY,
        'response': captcha_rs,
        'remoteip': get_client_ip(request)
	}
    verify_rs = requests.get(url, params=params, verify=True).json()
    return verify_rs['success']
    

def check_input_data(data):
	
    if hasattr(data, '_mutable'): data._mutable = True

    for key in data:
        if key not in ('user', 'url_id', 'long_url', 'password', 'recaptchaToken', 'expiration_date'):
            return {'error': "فیلد ناشناخته !"}

    if not url_validator_regex.match(data['long_url']):
        return {'error': 'لینک وارد شده اشتباه است !' + '\n' + 'توجه: لینک باید با //:http یا //:https شروع شود.'}

    if 'url_id' in data and data['url_id']:
        if data['url_id'] in ['registration', 'settings', 'report', 'admin']:
            return {'error': 'شما نمی توانید از این آدرس استفاده کنید !'}
        try:
            models.Link.objects.get(url_id=data['url_id'])
            return {'error': 'از این آدرس در یک لینک دیگر استفاده شده است !'}
        except models.Link.DoesNotExist:
            if not data['url_id'].isalnum():
                return {'error': 'در آدرس دلخواه از کاراکتر غیر مجاز استفاده شده است !'}
            elif len(data['url_id']) > 65:
                return {'error': 'حداکثر طول آدرس دلخواه 65 کاراکتر می باشد !'}


    if 'password' in data and data['password']:
        data['password'] = password_hashing(data['password'])


    if 'expiration_date' in data:
        if data['expiration_date']:
            date_str = data['expiration_date']
            try:
                date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                tomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
                if date < tomorrow:
                    return {'error': 'تاریخ وارد شده گذشته است !'}
                else:
                    data['expiration_date'] = date
            except:     
                return {'error': 'فرمت تاریخ وارد شده اشتباه است !'}
        else:
            del data['expiration_date']

    return data
