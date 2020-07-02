from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import PostForm,CommentForm
from django.views.decorators.http import require_POST, require_http_methods
from itertools import chain
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        posts=Post.objects.all()
        followings=request.user.followings.all()
        followings=chain(followings,[request.user])

        posts=Post.objects.filter(user__in=followings).order_by('id')
        comment_form=CommentForm()
        return render(request, 'index.html',{'posts':posts,'comment_form':comment_form})
    else:
        return redirect('posts:explore')

def explore(request):
    posts = Post.objects.order_by('id').all()
    comment_form = CommentForm()
    return render(request, 'index.html', {'posts':posts, 'comment_form':comment_form})


def dinner(request):
    menu=["족발","치킨","국수"]
    pick=random.choice(menu)

    return render(request,'dinner.html',{'dinner':pick})
def hello(request,name):
    return render(request, 'hello.html',{'name':name})

def throw(request):
    return render(request,'throw.html')

def catch(request):
    message=request.GET.get('message') #message라는 키값의 value를 가져오겠다.
    return render(request,'catch.html',{'message':message})

def naver(reqeust):
    return render(request,'naver.html')

def new(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    if request.method=='POST':
        post_form=PostForm(request.POST,request.FILES)

        if post_form.is_valid():
            post=post_form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('posts:list')
    else:
        post_form=PostForm()
    return render(request,'new.html',{'post_form':post_form})


def detail(request,post_id):
    post=Post.objects.get(pk=post_id)
    comment_form=CommentForm()
    return render(request, 'detail.html',{'post':post,'comment_form':comment_form})


def edit(request,post_id):

    post=Post.objects.get(pk=post_id)
    if post.user != request.user:
        return redirect('posts:list')
    if request.method=='POST':
        post.title = request.POST.get('title')
        post.content =request.POST.get('content')
        post.save()
        return redirect('posts:detail',post.pk)
    else:

        return render(request,'edit.html',{'posts':post})

def comments_create(request,post_id):
    post=get_object_or_404(Post,id=post_id)
    comment_form=CommentForm(request.POST)
    if comment_form.is_valid():
        comment=comment_form.save(commit=False)
        comment.user=request.user
        comment.post=post
        comment.save()

    return redirect('posts:detail',post.pk)


@require_http_methods(['GET','POST'])
def comments_delete(request, post_id, comment_id):
        comment=get_object_or_404(Comment, id=comment_id)

        comment.delete()

        return redirect('posts:detail', post_id)

def delete(request,post_id):

    if request.method=='POST':
        post=Post.objects.get(pk=post_id)
        if post.user != request.user:
            return redirect('posts:list')

        post.delete()
        return redirect('posts:list')
    else:
        return render(request,'delete.html')
    


def create(request):
    if request.method=='POST':
        pass
    else:
        return render(request,'create.html')


def comments_update(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
        return redirect('posts:detail', post_id)
    
    else:
        comment_form = CommentForm(instance=comment)
        return render(request, 'comment_update.html', {'comment_form':comment_form})

def like(request,post_id):
    if request.user.is_authenticated :
        post=get_object_or_404(Post,id=post_id)
        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)
    return redirect('posts:detail',post_id)
