from django.urls import path
from . import views

app_name = "shot"

urlpatterns = [
    path('', views.index, name='index'),
    path('loginsignup', views.loginsignup, name="loginsignup"),
    path('log_out', views.log_out, name="log_out"),
    path('logon', views.logon, name='logon'),
    path('signup', views.signup, name='signup'),
    path('hashtag/<str:hashtag_text>', views.hashtag, name='hashtag'),
    path('mention/<str:mention_text>', views.mention, name='mention'),
    path('post_shot', views.post_shot, name='post_shot'),
    path('author/<int:author_id>', views.author, name='author'),
    path('like/<int:shot_id>', views.like, name='like'),
    path('unlike/<int:shot_id>', views.unlike, name='unlike'),
    path('search', views.search, name='search'),
    path('follow/<int:author_id>', views.follow, name='follow'),
    path('unfollow/<int:author_id>', views.unfollow, name='unfollow'), 
    path('delete/<int:shot_id>', views.delete, name='delete'),
    path('comment/<int:shot_id>', views.post_comment, name='post_comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('like_comment/<int:comment_id>', views.like_comment, name='like_comment'),
    path('unlike_comment/<int:comment_id>', views.unlike_comment, name='unlike_comment'),
    path('popular', views.popular, name='popular'),
    path('post', views.post, name='post'),
    path('test', views.test, name='test')
]  