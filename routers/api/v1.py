from user.views import CreateUserView
from django.urls import path, include



urlpatterns = [
    path('', include("user.urls")),
    path('blog/', include("blog.urls")),
    path('blog/<int:pk>/comment/', include("comment.urls"))
]