from accounts.models import SocialUser
from accounts import serializers
from accounts.mixins import SocialLoginMixin, LogoutMixin
from accounts.serializers import JWTSerializer

from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema

import requests
from urllib.parse import urlencode
from json.decoder import JSONDecodeError
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


def kakao_login(request):  # TODO 프론트에서 담당
    authorize_url = "https://kauth.kakao.com/oauth/authorize"

    query_kwargs = {
        'client_id': getattr(settings, 'KAKAO_REST_API_KEY'),
        'redirect_uri': getattr(settings, 'BASE_URL') + reverse('kakao-callback'),
        'response_type': 'code',
    }
    return redirect(f'{authorize_url}?{urlencode(query_kwargs)}')


def kakao_callback(request):  # TODO 프론트에서 담당
    access_token_url = "https://kauth.kakao.com/oauth/token"

    query_kwargs = {
        'grant_type': 'authorization_code',
        'client_id': getattr(settings, 'KAKAO_REST_API_KEY'),
        'redirect_uri': getattr(settings, 'BASE_URL') + reverse('kakao-callback'),
        'code': request.GET.get("code"),
    }

    token_resp = requests.get(f'{access_token_url}?{urlencode(query_kwargs)}')
    token_resp_json = token_resp.json()
    error = token_resp_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    # access_token = token_resp_json.get("access_token")
    return JsonResponse(token_resp_json)


class SocialLoginView(generics.GenericAPIView, SocialLoginMixin):
    provider = None

    @swagger_auto_schema(
        responses={200: JWTSerializer}
    )
    def post(self, request, *args, **kwargs):  # TODO RAW data로 입력하면 GET으로 인식함
        return self.login(request, *args, **kwargs)


class KakaoLoginView(SocialLoginView):
    serializer_class = serializers.KaKaoLoginSerializer
    provider = 'kakao'


class SocialUserCreateView(generics.CreateAPIView, SocialLoginMixin):
    """
    회원가입
    """
    serializer_class = serializers.SocialUserCreateSerializer

    @swagger_auto_schema(
        responses={200: JWTSerializer}
    )
    def post(self, request, *args, **kwargs):
        self.provider = self.kwargs.get('provider')
        return self.signup(request, *args, **kwargs)


class SocialUserDeleteView(generics.DestroyAPIView):
    """
    회원탈퇴
    """
    queryset = SocialUser.objects.all()

    def perform_destroy(self, instance):
        user_delete_url = getattr(settings, 'UESR_API_BASE_URL') + f'user/users/{instance.id}'
        response = requests.delete(user_delete_url)
        response.raise_for_status()
        instance.delete()



class LogoutView(generics.GenericAPIView, LogoutMixin):
    pass
