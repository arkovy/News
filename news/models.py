from django.core.validators import MinLengthValidator
from django.db import models
from django.template.defaultfilters import slugify


class Tag(models.Model):
    caption = models.CharField(max_length=100)

    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)

    def full_name(self):
        return self.first_name + "" + self.last_name

    def __str__(self):
        return self.full_name()


class News(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=100)
    image_name = models.ImageField(upload_to='news', null=True)
    slug = models.SlugField(unique=True, db_index=True, blank=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='news', null=True)
    tags = models.ManyToManyField(Tag)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    user_name = models.CharField(max_length=30)
    user_email = models.EmailField()
    text = models.TextField(max_length=400)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')


