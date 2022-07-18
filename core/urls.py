from django.urls import  URLPattern, path
from . import views
urlpatterns=[
    path('', views.index , name='index'),
    path('signup', views.signup , name='signup'),
    path('signin', views.singin , name='signin'),
    path('profile/<str:pk>', views.profile , name='profile'),
    path('follow', views.follow , name='follow'),
    path('logout', views.logout , name='logout'),
    path('setting', views.setting , name='setting'),
    path('upload', views.upload , name='upload'),
    path('like', views.like , name='like'),
    path('search', views.search , name='search'),
    path('comment', views.comment , name='comment'),
    path('delete', views.delete , name='delete'),

]

