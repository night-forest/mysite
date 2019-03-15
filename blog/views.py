from django.shortcuts import get_object_or_404, render
from .models import Blog, BlogType
from django.core.cache import cache
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
# from comment.models import Comment
# from comment.forms import CommentForm
from user.forms import LoginForm
from read_statistics.utils import read_statistics_once_read, get_oneWeek_hotData
# Create your views here.
#连接models层，获取数据并在前端显示
def get_blog_list_common_data(request, blog_all_list):
    # blog_all_list = Blog.objects.all()
    # 分页器
    paginator = Paginator(blog_all_list, settings.EACH_BLOG_NUMBER)
    page_num = request.GET.get('page', 1)
    page_of_blog = paginator.get_page(page_num)
    curr_num = page_of_blog.number  # 获取当前页码
    # 获取当前页码前后各两页
    page_range = list(range(max(curr_num - 2, 1), curr_num)) + \
                 list(range(curr_num, min(curr_num + 2, paginator.num_pages) + 1))
    # 加上第一页和最后一页
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    #统计数量
    blog_datas = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_datas_dict = {}
    for blog_data in blog_datas:
        blog_count = Blog.objects.filter(create_time__year=blog_data.year, create_time__month=blog_data.month).count()
        blog_datas_dict[blog_data] = blog_count
    #阅读排行榜
    readOrder = cache.get('oneWeek_hotData')
    if readOrder is None:
        readOrder = get_oneWeek_hotData()
        cache.set('oneWeek_hotData', readOrder, 3600)
    context = {}
    # 等到所有博客的数据
    context['readOrder'] = readOrder
    context['blogs'] = page_of_blog.object_list  #当前页面的所有数据
    context['page_of_blog'] = page_of_blog  #当前页面
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_datas'] = blog_datas_dict
    # context['blog_count'] = Blog.objects.all().count()
    return context

def blog_list(request):
    blog_all_list = Blog.objects.all()
    #分页器
    context = get_blog_list_common_data(request, blog_all_list)
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_pk):
    context = {}
    #拿到不同博客的数据
    blog = get_object_or_404(Blog, pk=blog_pk)
    key = read_statistics_once_read(request, blog)
    # blog_content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_pk, parent=None)
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog'] = blog
    context['login_form'] = LoginForm()
    # context['comment_form'] = CommentForm(initial={'content_type': blog_content_type, 'object_id': blog_pk, 'reply_comment_id': 0})
    # context['comments'] = comments.order_by('-comment_time')
    response = render(request, 'blog/blog_detail.html', context)#响应
    response.set_cookie(key=key, value='true')
    return response

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    #分页器
    context = get_blog_list_common_data(request,blog_all_list)
    #等到所有博客的数据
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

def blog_with_data(request, year, month):
    blog_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)
    #分页器
    context = get_blog_list_common_data(request, blog_all_list)
    #等到所有博客的数据
    context['blog_with_data'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_with_data.html', context)
