from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Prediction
from .forms import PostForm
from django.shortcuts import redirect
import datetime as dt
from django.contrib.auth.decorators import login_required

import sys
sys.path.append('../')
from pred_keiba_data_reg import getPredResult


@login_required
def post_list(request):
	#日付新しい順
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	#日付古い順
	#posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(request.POST)
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	print(type(post))
	print(post)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def danraku(ls):
	temp_list = []
	temp = []
	for i in ls:
		temp.append(i)
		if((i+1) % 10) == 0:
			temp_list.append(temp)
			temp = []
	return temp_list


def forbun(request):
	ls = [i for i in range(100)]
	ls = danraku(ls)
	time_now = dt.datetime.now()
	print(time_now)
	return render(request,'blog/tesuto.html',{'list':ls, 'now':time_now})


def result(request):
	raceid = request.POST['raceid']
	print(raceid)
	print(type(raceid))
	temp = getPredResult(raceid)
	print(temp)
	Prediction.objects.create(raceid=raceid, ranking="")
	time_now = dt.datetime.now()
	return render(request,'blog/result.html',{'id':raceid,'now':time_now})