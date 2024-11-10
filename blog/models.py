from django.db import models
from django.utils import timezone

# Менеджер для получения только опубликованных постов и постов определенного автора
class PublishedManager(models.Manager):
    def published(self):
        # Возвращаем QuerySet, чтобы можно было продолжать фильтрацию
        return super().get_queryset().filter(published_date__lte=timezone.now())

    def by_author(self, author_name):
        # Возвращаем QuerySet, чтобы его можно было использовать с другими методами
        return self.get_queryset().filter(author=author_name)

# Модель для постов в блоге
class Post(models.Model):
    title = models.CharField(max_length=200)  # Заголовок поста
    content = models.TextField()  # Содержание поста
    author = models.CharField(max_length=100)  # Автор поста
    published_date = models.DateTimeField(default=timezone.now)  # Дата публикации
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    objects = PublishedManager()  # Применение кастомного менеджера

    def __str__(self):
        return self.title

# Модель для категорий постов
class Category(models.Model):
    name = models.CharField(max_length=100)  # Название категории
    posts = models.ManyToManyField(Post, related_name='categories')  # Связь "многие ко многим" с Post

    def __str__(self):
        return self.name

# Модель для комментариев к постам
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Связь с Post, при удалении поста удаляются комментарии
    author = models.CharField(max_length=100, default='Anonymous') # Автор комментария
    content = models.TextField()  # Текст комментария
    created_date = models.DateTimeField(auto_now_add=True)  # Дата создания комментария

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
