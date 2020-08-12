from django.urls import path
from rest_framework import routers

from .views import *

app_name = 'api'

router = routers.DefaultRouter()

urlpatterns = [
    path('', api_root),
]

urlpatterns += router.urls