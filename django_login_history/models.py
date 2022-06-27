

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver
from json import JSONDecodeError
from requests.exceptions import ConnectionError

import requests
import ipaddress



'''
Models
'''

class Login(models.Model):
    user        = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    ip          = models.CharField(max_length=15, null=True)
    external_ip = models.CharField(max_length=15, null=True)
    user_agent  = models.TextField()
    date        = models.DateTimeField(auto_now_add=True)
    country     = models.CharField(max_length=50, null=True)
    region      = models.CharField(max_length=50, null=True)
    city        = models.CharField(max_length=50, null=True)
    lon         = models.FloatField(default=0.0, null=True)
    lat         = models.FloatField(default=0.0, null=True)

    def __str__(self):
        return self.user.username + " (" + self.ip + ") at " + str(self.date)


def use_internet():
    if hasattr(settings, "DJANGO_LOGIN_HISTORY_USE_INTERNET"):
        return settings.DJANGO_LOGIN_HISTORY_USE_INTERNET
    else:
        return True


def get_client_ip(request):
    """
    :param request:
    :return:
    """

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip              = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    if not ip:
        raise(ConnectionError("No se ha podido obtener la IP"))

    return ip


def get_internal_external_ip(request):
    """
    :param request:
    :return:
    """

    iploc = get_client_ip(request)

    if ipaddress.ip_address(iploc).is_private:
        if hasattr(settings, 'IP_PLACEHOLDER'):
            iploc = settings.IP_PLACEHOLDER

    ipext = requests.get("https://api.ipify.org/?format=json").json().get("ip") if use_internet() else None

    return [iploc, ipext]


def get_location_data(request):
    """
    # if ip is local (so it's impossible to find lat/long coords and location)
    # project will use random google ip as placeholder]
    :param request:
    :return:
    """

    ips  = get_internal_external_ip(request)
    data = requests.get("http://ip-api.com/json/"+ips[1]).json() if use_internet() else {}

    data["ip"]          = ips[0]
    data["external_ip"] = ips[1]
    data["user_agent"]  =request.META['HTTP_USER_AGENT']

    return data


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    """
    :param sender:
    :param user:
    :param request:
    :param kwargs:
    :return:
    """

    try:
        location_info = get_location_data(request)
    except ConnectionError:
        location_info = {}
    except JSONDecodeError:
        location_info = {}

    Login.objects.create(
        user=user,
        ip=location_info.get("ip"),
        external_ip=location_info.get("external_ip"),
        user_agent=location_info.get("user_agent"),
        country=location_info.get("country"),
        region=location_info.get("region"),
        city=location_info.get("city"),
        lon=location_info.get("lon"),
        lat=location_info.get("lat"),
    )
