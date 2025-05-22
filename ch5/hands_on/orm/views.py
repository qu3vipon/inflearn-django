from django.shortcuts import render
from django.views.decorators.cache import cache_page


@cache_page(60)
def home_view(request):
    print("오래 걸리는 작업 진행 중...")
    return render(request, "email.html")
