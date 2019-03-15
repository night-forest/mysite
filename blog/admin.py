from django.contrib import admin
from .models import BlogType,Blog
# Register your models here.
#后显示的内容，用修饰器来
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type_name")
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', "title", "blog_type", "author", 'get_read_num', "create_time", "last_update_time")