from django.urls import path, include
from .views import *

app_name = 'base'

urlpatterns = [ 
                 
    path('', index, name='index'),
    path('profile', posts_of_following_profiles, name='my-profile'),
    path('new-post', new_post, name='new_post'),
    path('blogs', ProfileListView.as_view(), name='blogs-list-view'),  
    path('switch_follow', follow_unfollow_profile, name='follow-unfollow-view'),  
    path('blog/<pk>', ProfileDetailView.as_view(), name='profile-detail-view'),
    path('post/<pk>', get_post, name='post-detail-view'),
    
    path('read', read_post, name='read-post-view'),

]