from django.urls import path, re_path, include

from commonauth import views as commonauth_views

api_patterns = [
    path('users', commonauth_views.User.as_view()),
    path('token', commonauth_views.Token.as_view())
]
