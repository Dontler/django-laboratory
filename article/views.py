from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpRequest
from .models import Post
from django.template import Context
from django.template.loader import render_to_string
from .forms import SearchForm
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
    elif request.method == 'POST':
        print(request.body)
        q = request.body
        posts = Post.objects.filter(title__icontains=q)
        results = []
        for p in posts:
            results.append(p.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def post_search(request):
    if request.method == 'GET':
        return render(request, 'article/search.html', {'form': SearchForm()})
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data['query']
            posts = Post.objects.filter(text__icontains=q)
            context = {'query': q, 'posts': posts}
            s = render_to_string('article/post_search.html', {'query': q, 'posts': posts})
            return HttpResponse(json.dumps(s), 'application/json')
        else:
            redirect('/search')
