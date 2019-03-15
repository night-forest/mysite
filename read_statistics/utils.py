import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from blog.models import Blog
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        #总阅读数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
    #当天阅读量+1
        data = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=data)
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_sevent_day_read_data(content_type):
    '''
    获取前七天的阅读量
    :param content_type:
    :return:
    '''
    today = timezone.now().date()
    read_nums = []
    _datas = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        _datas.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums, _datas

def get_twoDay_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.\
        filter(content_type=content_type, date=today).\
        order_by('-read_num')
    return read_details[:7]

def get_oneWeek_hotData():
    '''
    获取总阅读量前七的数据
    :return: objects
    '''
    read_details = Blog.objects.all()\
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return read_details[:7]
