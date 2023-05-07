from django.urls import path
from . import views
from . import util
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from .views import ImageDownloadView

urlpatterns = [
    # path('', views.home, name="blog-home"),
    path('about/', views.about, name="blog-about"),
    path('search/', views.search, name = "search"),
    path('', PostListView.as_view(), name="blog-home"),
    path('post-new/', PostCreateView.as_view(), name="blog-new"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
    path('download-image/<int:pk>/', ImageDownloadView.as_view(), name='image_download'),
    path('colorize-image/', util.colorMyImg, name="colorize-image"),
  
]
     