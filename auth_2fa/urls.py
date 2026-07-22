from django.urls import path
from .views import RegisterView, LoginView, VerifyCodeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', VerifyCodeView.as_view(), name='verify'),
]