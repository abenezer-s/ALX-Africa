# notifications/urls.py
from django.urls import path
from .views import notification_list, mark_notification_as_read

urlpatterns = [
    path('', notification_list, name='notification_list'),
    path('<int:notification_id>/read/', mark_notification_as_read, name='mark_notification_as_read'),
]
