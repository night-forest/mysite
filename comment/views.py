from django.http import JsonResponse
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


def update_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent:
            comment.root = parent.root if parent.root else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        #发送邮件通知
        comment.send_mail()
        #返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_get_username()
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if parent:
            data['reply_to'] = comment.reply_to.get_nickname_or_get_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
    return JsonResponse(data)
