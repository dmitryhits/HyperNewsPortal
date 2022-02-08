from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.http import Http404
import json
from datetime import datetime
from random import randint


with open(settings.NEWS_JSON_PATH) as f:
    news_list = json.load(f)
# Create your views here.


def under_construction(request):
    return redirect('/news/')
    # return render(request, 'news/index.html')


def head_news(request):
    news_links = {}
    selected_news = []
    query = request.GET.get('q')
    if query:
        print(f'query: {query}')
        selected_news = [newslet for newslet in news_list if query in newslet['title']]
        print(selected_news)
    else:
        selected_news = news_list.copy()
    for newslet in selected_news:
        date = datetime.fromisoformat(newslet['created']).date().strftime('%Y-%m-%d')
        news_links.setdefault(date, []).append(newslet)
    # sort by date in reverse order
    news_links = dict(sorted(news_links.items(), reverse=True))
    return render(request, 'news/news_main.html', context={'news_links': news_links})


def news(request, news_id):
    context = {}
    for newslet in news_list:
        if newslet['link'] == news_id:
            context = newslet
    if context:
        return render(request, 'news/newslet.html', context=context)
    else:
        raise Http404



class News(View):
    news = news_list
    links = [item['link'] for item in news_list]

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        text = request.POST.get('text')
        created = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        while True:
            link = randint(0, 10000)
            if link not in self.links:
                break
        newslet = {'created': created, 'text': text, 'title': title, 'link': link}
        self.news.append(newslet)
        with open(settings.NEWS_JSON_PATH, 'w+') as f_json:
            json.dump(self.news, f_json)
        return redirect('/news/')

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')
