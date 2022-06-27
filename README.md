### django-login-history

Plug-in django app that once included, stores logins history (with device data, like IP, user-agent, location etc.) of all users.


# Setup

1. Install this app using ``` pip install django-login-history ```
2. Include this app in your ```settings.py```  ```INSTALLED_APPS``` list:

```
INSTALLED_APPS = [  
    '...',  
    'django_login_history'  
]
```

That's it! You can login to admin panel and check how data is stored!

# Additional setup configuration:

If you are requesting django server from LAN (calling it by 192.XXX.XXX.XXX or localhost), which you are doing 99% times when you are developing this app cannot get your real location data. That's why this app needs to use some public IPs as placeholder, so it can populate rows with dummy data. You can change placeholder IP in your settings, for example:

```
IP_PLACEHOLDER = "172.217.23.195"
```

If you don't want to connect to the Internet to get IP information, you can define DJANGO_LOGIN_HISTORY_USE_INTERNET in your settings files: 

```
DJANGO_LOGIN_HISTORY_USE_INTERNET = False
```

# License
MIT License
