from django.urls import re_path
from .views import depsoit_view, PaymentMethodView, bot_view, close_trade, trading_account_view,\
    page

urlpatterns = [
    re_path('deposit/(?P<slug>[-\w]+)/', depsoit_view, name='deposit'),
    re_path('payment-method/', PaymentMethodView.as_view(), name='payment-method'),
    re_path('bot/', bot_view, name='bot'),
    re_path('page/', page, name='page'),
    re_path('close-trade/', close_trade, name='close-trade'),
    re_path('trading-account/', trading_account_view, name='trading-account'),
]