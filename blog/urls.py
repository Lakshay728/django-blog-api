from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_post_page, name='create-post'),
    path('api/posts/', views.post_list, name='post-list'),
    path('api/posts/<int:pk>/', views.post_detail, name='post-detail'),
]