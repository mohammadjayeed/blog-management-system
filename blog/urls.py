from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('', views.BlogCreateViewSet.as_view({'post': 'create', 'get': 'list'}), name='blog'),
    path('me/', views.BlogCreateViewSet.as_view({'get': 'me'}), name='blog-own'),
    path('<int:pk>/', views.BlogRetrieveUpdateDeleteViewSet.as_view({'get':'retrieve',
                                                                     'put': 'update',
                                                                     'delete':'destroy'}), name = 'blog-details'),                                                          

]