from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from questions.views import QuestionViewSet
from accounts.views import CustomUserViewSet
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

router.register(r"questions", QuestionViewSet)
router.register(r"accounts", CustomUserViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("questions.urls")),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('social_django.urls', namespace='social')),
    path("accounts/", include("accounts.urls")),
    path("pesapal/", include("pesapal.urls")),
    path("contacts/", include("contacts.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
