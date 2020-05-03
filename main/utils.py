import requests
from Api.models import Click


def UserCountry(ip):
	return requests.get("https://freegeoip.app/json/" + ip).json()['country_name']


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_click_details(request, url_obj):
	# get user device
	ua = request.user_agent
	try:
		device = {
			ua.is_pc: 'PC',
			ua.is_touch_capable: 'Touch Capable',
			ua.is_mobile: 'Mobile',
			ua.is_tablet: 'Tablet',
		}[True]
	except KeyError:
		device = 'Other'
	
	url_obj.views_count += 1
	url_obj.save()
	Click(
		short_url=url_obj,
		browser=ua.browser.family,
		os=ua.os.family,
		device=device,
		country=UserCountry(get_client_ip(request))
	).save()
