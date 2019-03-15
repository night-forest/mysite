from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
# Create your models here.
#建议数据库的表
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    #把后端的名称转为正常的字符串=
    def __str__(self):
        return self.type_name

class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail) #反向关联到ReadDetail数据库
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def get_email(self):
        return self.author.email
    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})
    def __str__(self):
        return "<Blog: %s>" % self.title
    class Meta:
        ordering = ['-create_time']



