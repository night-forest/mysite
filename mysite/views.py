from django.shortcuts import render
from django.core.cache import cache
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_sevent_day_read_data, get_twoDay_data, get_oneWeek_hotData

def home(request):
    ct = ContentType.objects.get_for_model(Blog)
    read_num, data = get_sevent_day_read_data(ct)
    today_hot = get_twoDay_data(ct)
    Week_hot = cache.get('oneWeek_hotData')
    if cache.get('oneWeek_hotData') is None:
        Week_hot = get_oneWeek_hotData()
        cache.set('oneWeek_hotData', Week_hot, 3600)
        print('set cache')
    print('get cache')
    context = {}
    context['read_num'] = read_num
    context['date'] = data
    context['today_hot'] = today_hot
    context['Week_hot'] = Week_hot
    return render(request, 'home.html', context)
