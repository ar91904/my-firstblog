from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm, LoginForm, UserRegistrationForm
from django.shortcuts import redirect
from django .core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    # If logged in can access dashboard
    return render(request,'blog/dashboard.html', {'section': 'dashboard'})



def post_list(request):
    object_list = Post.objects.filter(created_date__lte=timezone.now()).order_by('published_date')

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
    return render(request, 'blog/post_list.html', {'posts': posts, 
                                                   'page': page})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk,)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    comment_form = CommentForm(data=request.POST)

    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign current post to comment
            new_comment.post = post
            # Save the comment to database
            new_comment.save()
        else:
            comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            # Don't save post yet
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now() + timezone.timedelta(days=7)
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
        # Redirects back to main page
        return redirect('/')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

def register(request):
    if request.method == ("POST"):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create new user object but avoid saving it 
            new_user = user_form.save(commit=False)
            # Set chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the user object
            new_user.save()
            return render(request, 'blog/register_done.html', 
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', 
                  {'user_form': user_form})
