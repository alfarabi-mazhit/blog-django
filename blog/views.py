from django.shortcuts import redirect,render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post
from .forms import PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    def get_queryset(self):
        queryset = Post.objects.published()  # Начинаем с опубликованных постов
        author_name = self.request.GET.get('author')  # Получаем автора из параметров запроса
        if author_name:  # Если параметр author есть, фильтруем по нему
            queryset = queryset.filter(author__icontains=author_name)
        return queryset

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    pk_url_kwarg = 'post_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            form.save_m2m()  # сохраняем многие-ко-многим данные (категории)
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form})
