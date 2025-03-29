from django.contrib import admin
from news.models import News, Author, Tag, Comment


class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_filter = ('title', 'tags', 'date')
    list_display = ('title', 'date', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'news')


admin.site.register(News, NewsAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment)
