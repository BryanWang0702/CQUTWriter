from django.http import JsonResponse
from django.shortcuts import render
from Generate.generateApp import GenerateApp

generateApp = GenerateApp()


# Create your views here.
def locate_generate_by_title(request):
    return render(request, "generate_by_title.html")


def locate_generate_by_abstract(request):
    return render(request, 'generate_by_abstract.html')


def locate_generate_by_outline(request):
    return render(request, 'generate_by_outline.html')


def locate_generate_by_template(request):
    return render(request, 'generate_by_template.html')


def get_abstract(request):
    """
    根据标题和关键词检索摘要
    :param request:
    :return:
    """

    title = request.POST.get("title")
    keywords = request.POST.get("keywords")
    generateApp.get_abstract(title=title, keywords=keywords)

    outputContent = {
        'abstract': generateApp.abstract
    }

    return JsonResponse(outputContent, json_dumps_params={'ensure_ascii': False})


def get_outline(request):
    """
    根据标题和关键词检索摘要
    :param request:
    :return:
    """

    title = request.POST.get("title")
    keywords = request.POST.get("keywords")
    generateApp.get_outline(title=title, keywords=keywords)

    outputContent = {
        'outline': generateApp.outline
    }

    return JsonResponse(outputContent, json_dumps_params={'ensure_ascii': False})


def generate_by_title(request):
    """
    根据标题生成
    :param request:
    :return:
    """
    title = request.POST.get("title")
    keywords = request.POST.get("keywords")

    generateApp.title_generate(title, keywords)

    outputContent = {
        'article': generateApp.article
    }

    return JsonResponse(outputContent, json_dumps_params={'ensure_ascii': False})


def generate_by_abstract(request):
    """
    根据摘要生成
    :param request:
    :return:
    """
    title = request.POST.get("title")
    keywords = request.POST.get("keywords")
    abstract = request.POST.get("abstract")

    generateApp.abstract_generate(title, keywords, abstract)

    outputContent = {
        'article': generateApp.article
    }

    return JsonResponse(outputContent, json_dumps_params={'ensure_ascii': False})


def generate_by_outline(request):
    """
    根据大纲生成
    :param request:
    :return:
    """
    title = request.POST.get("title")
    keywords = request.POST.get("keywords")
    abstract = request.POST.get("abstract")
    outline = request.POST.get("outline")

    generateApp.outline_generate(title, keywords, abstract, outline)

    outputContent = {
        'article': generateApp.article
    }

    return JsonResponse(outputContent, json_dumps_params={'ensure_ascii': False})

