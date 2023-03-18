from django.shortcuts import render
from News.newsApp import NewsApp

newsApp = NewsApp()


# Create your views here.
def news(request):
    content = {
        'daily_news': newsApp.news
    }

    return render(request, 'news.html', content)
