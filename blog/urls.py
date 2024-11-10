from django.urls import path
from . import views 

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('add/', views.add_post, name='add_post'),
    path('<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
]
