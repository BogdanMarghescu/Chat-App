from django.urls import path, include
from rest_framework.routers import DefaultRouter

from profiles_api import views

router = DefaultRouter()
router.register('register', views.UserProfileViewSet)

urlpatterns = [
    path('login/', views.UserLoginApiView.as_view()),
    path('send-message/', views.MessageSendApiView.as_view()),
    path('get-messages/', views.MessageViewApiView.as_view()),
    path('', include(router.urls)),
]
