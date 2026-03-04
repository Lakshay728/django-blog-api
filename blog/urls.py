from django.urls import path , include
from . import views # pyright: ignore[reportMissingImports]

urlpatterns = [
    path('', views.home, name='home'),
    path('api/posts/', views.post_list, name='post-list'),
    path('api/posts/<int:pk>/', views.post_detail, name='post-detail'),
]