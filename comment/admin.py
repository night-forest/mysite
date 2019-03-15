from django.contrib import admin
from .models import Comment
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'comment_time', 'content_object', 'comment_time', 'text', 'parent_id')
