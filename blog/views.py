from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django .core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    object_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    
    page = request.GET.get('page')
    paginator = Paginator(object_list, 3) # 3 posts per page
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': page})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
    return render(request, 'blog/post_edit.html', {'form': form , 'post' : post} )

def deleteTodoItem(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        print(pk)
        y = Post.objects.get(pk=pk)
        y.delete()
        return redirect('/')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})



