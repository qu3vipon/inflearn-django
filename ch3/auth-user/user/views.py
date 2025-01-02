import uuid

import requests

from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from django.conf import settings
from user.forms import CustomUserCreationForm
from user.models import CustomUser


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class SignUpView(View):
    def get(self, request):
        return render(
            request, "sign_up.html",
            {"form": CustomUserCreationForm}
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("home"))


class KakaoSocialLoginView(View):
    def get(self, request):
        return redirect(
            f"https://kauth.kakao.com/oauth/authorize"
            f"?client_id={settings.KAKAO_REST_API_KEY}"
            f"&redirect_uri={settings.KAKAO_CALLBACK_URL}"
            f"&response_type=code"
        )


class KakaoSocialCallbackView(View):
    def get(self, request):
        auth_code = request.GET.get("code")

        # 카카오에 access_token 요청
        response = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.KAKAO_REST_API_KEY,
                "redirect_uri": settings.KAKAO_CALLBACK_URL,
                "code": auth_code,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
            }
        )

        if response.ok:
            access_token = response.json().get("access_token")

            # 카카오 프로필 조회
            profile_response = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if profile_response.ok:
                username = f"K#{profile_response.json()['id']}"

                try:
                    # 이미 회원인 경우
                    user = CustomUser.objects.get(username=username)
                except CustomUser.DoesNotExist:
                    user = CustomUser.objects.create_user(username=username, password=str(uuid.uuid4()))

                # 세션 로그인
                login(request, user)
                return redirect(reverse("home"))
        return JsonResponse({"error": "Social Login Failed.."})
