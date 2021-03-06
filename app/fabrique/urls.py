"""fabrique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('', include('api.urls', namespace='api')),
    path('favicon.ico',
         RedirectView.as_view(url='/static/img/favicon.png'),
         name='favicon'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
