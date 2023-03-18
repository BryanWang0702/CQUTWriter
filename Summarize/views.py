from django.http import JsonResponse
from django.shortcuts import render
from Summarize.summarizeApp import SummarizeApp

summarizeApp = SummarizeApp()


# Create your views here.

def locate_summarize(request):
    return render(request, 'summarize.html')


def summarize(request):
    """
    生成摘要和关键词
    :param request:
    :return:
    """

    inputContent = request.POST.get("inputContent")

    abstract, keywords = summarizeApp.abstract_keywords_generation(inputContent)

    outputContent = {
        'abstract': abstract,
        'keywords': keywords
    }

    return JsonResponse(outputContent, json_dumps_params={'ensure_ascii': False})
