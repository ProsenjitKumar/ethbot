from django.urls import re_path
from .views import *

urlpatterns = [
    re_path('withdraw-data/', withdraw_view, name='withdraw-data'),
]