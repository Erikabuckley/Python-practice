from django.urls import path, re_path
from .views import index, PostListView, PostDetailView, CommentListView, TestTemplateView
from forum.forum_feeds import LatestPostFeed

urlpatterns = [
    path('',index, name="index"),
    path('latest/posts/',LatestPostFeed()),
    path('<int:pk>/', PostDetailView.as_view(), name="detail"),
    path('test', TestTemplateView.as_view(), name='template'),
    path('<int:post_id>/comment/', CommentListView.as_view(), name="comment"),
    
    re_path(r'^posts/(?P<year>[0-9]{4})/$', PostListView.as_view(), name='by_year'),
    re_path(r'^posts/(?P<year>[0-9]{4})/(?P<month>[0-9]{4})/$', PostListView.as_view(), name='by_month'),
    #re_path(r'^posts/(?P<year>[0-9]{4})/(?P<month>[0-9]{4})/(?P<slug>[\w-]+{4})/$', DetailView.as_view() , name='slug_detail'),    
]