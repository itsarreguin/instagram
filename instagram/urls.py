"""Instagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Python standard library
from typing import List

# Django urls
from django.urls import path
from django.urls import include
# Django contrib
from django.contrib import admin
# Django config
from django.conf import settings
from django.conf.urls.static import static


urlpatterns: List[path] = [
    path(
        route='',
        view=include('instagram.account.urls', namespace='account')
    ),
    path(
        route='',
        view=include('instagram.posts.urls', namespace='posts')
    ),
    path(
        route='',
        view=include('instagram.notifications.urls', namespace='notifications')
    ),
    path(
        route='',
        view=include('instagram.messenger.urls', namespace='messenger')
    )
]

if settings.DEBUG:
    urlpatterns += [
        path('django/admin/', admin.site.urls),
        path('__debug__/', include('debug_toolbar.urls'))
    ]
    urlpatterns += static(
        settings.MEDIA_URL, document_root = settings.MEDIA_ROOT
    )