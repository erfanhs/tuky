from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_GET

from Api.models import User, Link, Token

from .utils import save_click_details
from django.utils import timezone


@require_GET
def handle_link(request, url_id):
	url = get_object_or_404(Link, url_id=url_id)
	if url.expired:
		return render(request, 'handleLinkError.html', context={'expired': True})
	elif url.banned:
		return render(request, 'handleLinkError.html')
	
	if url.password:
		return render(request, 'askLinkPassword.html', context={'url_id': url_id})

	save_click_details(request, url)

	response = HttpResponse(status=302)
	response['Location'] = url.long_url
	return response


@require_GET
def verify(request, verify_id):
	try:
		user = User.objects.get(email_verify=verify_id)
		user.last_login_at = timezone.now()
		user.email_verify = 'verified'
		user.verified = True
		user.save()

		user_token = get_random_string(length=40)
		Token.objects.create(user=user, token=user_token)

		User.objects.filter(~Q(email_verify='verified'), email=user.email).delete()

		return render(request, 'email_verified.html', context={'token': user_token, 'email': user.email})
	except User.DoesNotExist:
		return redirect('registration')
	

@require_GET
def index(request): return render(request, 'index.html')
@require_GET
def registration(request): return render(request, 'registration.html')
@require_GET
def settings_(request): return render(request, 'settings.html')
@require_GET
def report(request): return render(request, 'report.html')
@require_GET
def stats(request, url_id): return render(request, 'stats.html')
