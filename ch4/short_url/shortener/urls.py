from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shortener import views, api
from shortener.api import ShortURLViewSet

router = DefaultRouter()
router.register(
    "api/short-urls",
    ShortURLViewSet,
    "short_urls",
)


urlpatterns = [
    # django
    path("", views.HomeView.as_view(), name="home"),
    path("short-urls/", views.ShortURLCreateView.as_view(), name="shorten_url"),
    path("<str:code>/", views.ShortURLDetailView.as_view(), name="short_url_detail"),

    # drf
    # path("api/short-urls/", api.ShortURLAPIView.as_view(), name="short_urls_api"),
    # path("api/short-urls/<str:code>/", api.ShortURLDetailAPIView.as_view(), name="short_url_detail_api"),

    # view set
    path("", include(router.urls)),
]
