from django.urls import path
from . import views


urlpatterns = [
    path('', views.CommentCreateViewSet.as_view({'post': 'create'}), name='comment'),                                                         

]