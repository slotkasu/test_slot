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

# 予想結果を返すくん
def result(request):
	
	if request.method =="POST":
		# リクエストからraceidを抜き出します
		raceid = request.POST['raceid']
	else:
		return render(request,'blog/result.html',{"warning": "INVALID METHOD TO PREDICT."})
	
	# raceidが12桁かどうかを判定
	if len(raceid)!=12:
		return render(request,'blog/result.html',{"warning": "INVALID RACEID."})
	# 既に予想してるかどうか
	temp = Prediction.objects.filter(raceid=raceid)
	# してた
	if temp:
		print("already exist")
	# してない
	else:
		# 予想します
		temp = getPredResult(raceid)
		# 今の時間
		nowtime = dt.datetime.now()
		# 予想結果を保存
		Prediction.objects.create(raceid=raceid, ranking=temp, req_time=nowtime)

	# 戻り値
	ret = Prediction.objects.get(raceid=raceid)
	return render(request,'blog/result.html',{"atai":ret})