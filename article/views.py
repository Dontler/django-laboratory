from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Post
from django.utils import timezone
import json

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'article/post_detail.html', {'post': post})


def main_title(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'article/post_list.html', {'posts': posts})


def search(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Post.objects.filter(title__startswith=q)
        results = []
        print(q)
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
