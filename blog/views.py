from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from blog.models import Post, Comment
from blog.forms import CommentForm


@cache_page(60 * 15)  # Cache for 15 minutes
def blog_index(request):
    """Display all active blog posts with optimized queries."""
    posts = Post.objects.filter(
        is_active=True
    ).prefetch_related('categories').order_by("-created_on")
    
    context = {"posts": posts}
    return render(request, "blog/blog_index.html", context)


@cache_page(60 * 15)  # Cache for 15 minutes
def blog_category(request, category):
    """Display blog posts filtered by category with optimized queries."""
    posts = Post.objects.filter(
        categories__name__contains=category,
        is_active=True
    ).prefetch_related('categories').order_by("-created_on")
    
    context = {"category": category, "posts": posts}
    return render(request, "blog/blog_category.html", context)


@cache_page(60 * 60)  # Cache for 1 hour
def blog_detail(request, pk):
    """Display single blog post with comments."""
    post = get_object_or_404(
        Post.objects.prefetch_related('categories'),
        pk=pk,
        is_active=True
    )

    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment.save()

    comments = Comment.objects.filter(post=post).order_by('-created_on')
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }

    return render(request, "blog/blog_detail.html", context)
