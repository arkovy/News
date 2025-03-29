from django.utils.text import slugify
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from news.models import News, Author
from django.views.generic import ListView, View
from .forms import CommentForm, NewsForm


class IndexView(ListView):
    template_name = 'news/index.html'
    model = News
    ordering = '-date'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:10]
        return data


class SignUp(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('starting-page')  # Перенаправление на главную страницу
        return render(request, 'registration/signup.html', {'form': form})


class AddNewsView(LoginRequiredMixin, View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'news/add-news.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            author, created = Author.objects.get_or_create(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email
            )
            news.author = author
            news.slug = slugify(news.title)  # Генерируем slug из заголовка

            # Проверяем, существует ли уже такой slug
            original_slug = news.slug
            counter = 1
            while News.objects.filter(slug=news.slug).exists():
                news.slug = f"{original_slug}-{counter}"
                counter += 1

            try:
                news.save()
                return redirect('news-page')
            except IntegrityError:
                form.add_error(None, "Ошибка: такой заголовок уже существует.")

        return render(request, 'news/add-news.html', {'form': form})


class AllNewsView(LoginRequiredMixin, ListView):
    template_name = 'news/all-news.html'
    model = News
    ordering = '-date'
    context_object_name = 'all_news'


class SingleNewsView(View):
    def is_stored_news(self, request, news_id):
        stored_news = request.session.get('stored_news')

        if stored_news is not None:
            is_saved_for_later = news_id in stored_news
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        news = News.objects.get(slug=slug)
        stored_news = request.session.get('stored_news')

        context = {
            'news': news,
            'news_tags': news.tags.all(),
            'comment_form': CommentForm(),
            'comments': news.comments.all().order_by('-id'),
            'is_saved_for_later': self.is_stored_news(request, news.id)
        }
        return render(request, 'news/news-detail.html', context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        news = News.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.news = news
            comment.save()

            return HttpResponseRedirect(reverse('news-detail-page', args=[slug]))

        context = {
            'news': news,
            'news_tags': news.tags.all(),
            'comment_form': CommentForm(),
            'comments': news.comments.all().order_by('-id'),
            'is_saved_for_later': self.is_stored_news(request, news.id)
        }
        return render(request, 'news/news-detail.html', context)


class ReadLaterView(View):
    def get(self, request):
        stored_news = request.session.get('stored_news')

        context = {}

        if stored_news is None or len(stored_news) == 0:
            context['news'] = []
            context['has_news'] = False
        else:
            news = News.objects.filter(id__in=stored_news)
            context['news'] = news
            context['has_news'] = True

        return render(request, 'news/stored-news.html', context)

    def post(self, request):
        stored_news = request.session.get('stored_news')

        if stored_news is None:
            stored_news = []

        news_id = int(request.POST['news_id'])

        if news_id not in stored_news:
            stored_news.append(news_id)
        else:
            stored_news.remove(news_id)

        # Сохраняю обновленный список в сессии
        request.session['stored_news'] = stored_news

        # Перенаправляю на страницу с отложенными новостями
        return redirect('read-later')
