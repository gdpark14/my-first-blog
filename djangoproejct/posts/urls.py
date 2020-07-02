"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from posts import views
from django.urls import include

app_name='posts'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index ,name='list'),
    path('dinner/',views.dinner),
    path('hello/<str:name>/',views.hello),#URL주소로 들어오는 값을 변수로 지정
    path('throw/',views.throw),
    path('catch/',views.catch),
    path('naver/',views.naver),
    path('new/',views.new, name='new'),
    path('<int:post_id>/',views.detail, name='detail'),
    path('<int:post_id>/delete/',views.delete, name='delete'),
    path('<int:post_id>/edit/',views.edit, name='edit'),
    path('<int:post_id>/like/',views.like, name='like'),
    path('explore/',views.explore,name='explore'),

    path('<int:post_id>/comments/create/',views.comments_create,name='comments_create'),
    path('<int:post_id>/comments/<int:comment_id>/delete/',views.comments_delete, name='comments_delete'),
    path('<int:post_id>/comment/<int:comment_id>/update/', views.comments_update, name="comments_update")
]
