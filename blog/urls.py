from django.urls import path
from . import views

urlpatterns=[
    #不同的博客显示不同的内容
    path('', views.blog_list, name="blog_list"),
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blogs_with_type, name="blogs_with_type"),
    path('data/<int:year>/<int:month>', views.blog_with_data, name="blog_with_data"),

]