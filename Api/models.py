from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings

import qrcode
import os


class User(models.Model):
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=40)
	signup_at = models.DateTimeField(default=timezone.now)
	last_login_at = models.DateTimeField(blank=True, null=True)
	email_verify = models.CharField(max_length=32, blank=True)
	verified = models.BooleanField(default=False)

	def __str__(self):
		return self.email


class Token(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	token = models.CharField(max_length=40)

	def __str__(self):
		return self.user.email


class Link(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	url_id = models.CharField(max_length=65, blank=True)
	long_url = models.TextField()
	password = models.CharField(max_length=40, blank=True)
	has_password = models.BooleanField(default=False)
	dateTime = models.DateTimeField(default=timezone.now)
	expiration_date = models.DateTimeField(blank=True, null=True)
	views_count = models.IntegerField(default=0)
	qr_img = models.ImageField(blank=True)
	expired = models.BooleanField(default=False)
	banned = models.BooleanField(default=False)

	def save(self, *args, **kwargs):
		if not self.url_id:
			self.url_id = get_random_string(length=6)
		if self.password:
			self.has_password = True
		
		if self.user:
			qr_img_path = './Api/QRs/' + self.url_id + '.png'
			qr = qrcode.make(('http://%s/' % settings.HOST_NAME) + self.url_id)
			qr.save(qr_img_path)
			self.qr_img = qr_img_path

		super(Link, self).save(*args, **kwargs)

	def delete(self, *args, **kwargs):
		if self.user:
			os.remove('./Api/QRs/' + self.url_id + '.png')
		super(Link, self).delete(*args, **kwargs)

	def __str__(self):
		return self.url_id + '   -   ' + self.long_url



class Click(models.Model):
	short_url = models.ForeignKey(Link, on_delete=models.CASCADE)
	dateTime = models.DateTimeField(default=timezone.now)
	os = models.CharField(max_length=20)
	browser = models.CharField(max_length=20)
	device = models.CharField(max_length=20)
	country = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return str(self.dateTime)


class Report(models.Model):
	short_url = models.ForeignKey(Link, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.short_url)
