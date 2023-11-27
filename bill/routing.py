from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bill/(?P<bill_id>\w+)/$', consumers.BillConsumer.as_asgi()),
]