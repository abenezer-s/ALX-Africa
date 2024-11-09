from django.urls import path, include
from .views import BookView
from rest_framework.routers import DefaultRouter
from .views import BookListViewSet

router = DefaultRouter()
router.register(r'BookListViewSet', BookListViewSet, basename='BookListViewSet')

urlpatterns = [
    path('',include('router.urls'))
]