from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('', views.BlogViewSet.as_view({'post': 'create'}), name='blog'),
    path('<int:pk>/', views.BlogRetrieveUpdateDeleteViewSet.as_view({'get': 'retrieve', 'put': 'update','delete':'destroy'}), name = 'blog-details'),
]