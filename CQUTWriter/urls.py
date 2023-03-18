"""CQUTWriter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Home.views import home, home_generate
from News.views import news
from Generate.views import locate_generate_by_title, locate_generate_by_abstract, locate_generate_by_outline, \
    locate_generate_by_template, get_abstract, get_outline, generate_by_title, generate_by_abstract, generate_by_outline

from Summarize.views import locate_summarize, summarize

urlpatterns = [
    path('admin/', admin.site.urls),

    # 定位到各个页面
    path('', home, name='home'),
    path('news/', news, name='news'),
    path('titleGenerate/', locate_generate_by_title, name='locate_generate_by_title'),
    path('abstractGenerate/', locate_generate_by_abstract, name='locate_generate_by_abstract'),
    path('outlineGenerate/', locate_generate_by_outline, name='locate_generate_by_outline'),
    path('templateGenerate/', locate_generate_by_template, name='locate_generate_by_template'),
    path('summarize/', locate_summarize, name='locate_summarize'),

    # 各个js调用
    path('titleGenerate/generate/', generate_by_title),
    path('abstractGenerate/generate/', generate_by_abstract),
    path('outlineGenerate/generate/', generate_by_outline),
    path('get_abstract/', get_abstract),
    path('get_outline/', get_outline),
    path('summarize/summarize/', summarize),
    path('home/generate/', home_generate)
]
