from django.http import JsonResponse
from django.shortcuts import render
from Home.homeApp import HomeApp

homeApp = HomeApp()


# Create your views here.
def home(request):
    return render(request, 'home.html')


def home_generate(request):
    """
    根据前端传过来的标题和首句，返回一段已经续写好的文本
    :param request:
    :return:
    """

    title = request.POST.get("title")
    sentence = request.POST.get("sentence")

    outputContent = {
        "outputContent": homeApp.get_text(title, sentence)
    }

    return JsonResponse(outputContent, json_dumps_params={'ensure_ascii': False})
